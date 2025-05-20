from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ScanRecord
from impacket.dcerpc.v5.dcom import wmi
from impacket.dcerpc.v5.dcomrt import DCOMConnection
from impacket.dcerpc.v5.dtypes import NULL
import socket
import re
import logging

logger = logging.getLogger(__name__)

def validate_ipv4(ip):
    pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return bool(re.match(pattern, ip))

def resolve_netbios_to_ip(netbios_name):
    try:
        return socket.gethostbyname(netbios_name)
    except socket.gaierror:
        return None

def scan_machine(request):
    if request.method == 'POST':
        netbios_name = request.POST.get('netbios_name', '').strip()
        ipv4_address = request.POST.get('ipv4_address', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        action = request.POST.get('action', '')

        # Validate inputs
        if not netbios_name and not ipv4_address:
            messages.error(request, "At least one of NetBIOS name or IPv4 address is required.")
            return render(request, 'scan_hardware/scan.html')

        # Resolve NetBIOS to IP if provided
        target_ip = ipv4_address
        if netbios_name and not ipv4_address:
            target_ip = resolve_netbios_to_ip(netbios_name)
            if not target_ip:
                messages.error(request, f"Could not resolve NetBIOS name '{netbios_name}' to an IP address.")
                return render(request, 'scan_hardware/scan.html')

        # Validate IP
        if target_ip and not validate_ipv4(target_ip):
            messages.error(request, f"Invalid IPv4 address: {target_ip}")
            return render(request, 'scan_hardware/scan.html')

        if action in ['scan', 'save', 'cancel']:
            if action == 'scan':
                hardware_details = {}
                software_details = {}
                dcom = None
                iWbemServices = None
                iRegProvServices = None
                try:
                    # Connect to target via WMI
                    dcom = DCOMConnection(target_ip, username, password, domain='', oxidResolver=True)
                    iWbemLevel1Login = dcom.CoCreateInstanceEx(wmi.CLSID_WbemLevel1Login, wmi.IID_IWbemLevel1Login)
                    iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2', NULL, NULL)
                    iWbemLevel1Login.RemRelease()

                    # Hardware: RAM
                    total_ram = 0
                    for mem in iWbemServices.ExecQuery("SELECT Capacity FROM Win32_PhysicalMemory"):
                        total_ram += int(mem.Capacity) / (1024 ** 3)
                    hardware_details['ram'] = f"{total_ram:.2f} GB"

                    # Hardware: HDD/SSD
                    drives = []
                    for disk in iWbemServices.ExecQuery("SELECT Model, Size FROM Win32_DiskDrive"):
                        size = int(disk.Size) / (1024 ** 3) if disk.Size else 0
                        drives.append({
                            'model': disk.Model or 'Unknown',
                            'size': f"{size:.2f} GB",
                            'type': 'SSD' if 'SSD' in (disk.Model or '').upper() else 'HDD'
                        })
                    hardware_details['drives'] = drives

                    # Hardware: Processor
                    for cpu in iWbemServices.ExecQuery("SELECT Name, CurrentClockSpeed, NumberOfCores, ThreadCount FROM Win32_Processor"):
                        hardware_details['processor'] = {
                            'name': cpu.Name or 'Unknown',
                            'speed': f"{cpu.CurrentClockSpeed or 0} MHz",
                            'cores': cpu.NumberOfCores or 0,
                            'threads': cpu.ThreadCount or 0
                        }

                    # Hardware: Motherboard
                    for board in iWbemServices.ExecQuery("SELECT Manufacturer, Product, SerialNumber FROM Win32_BaseBoard"):
                        hardware_details['motherboard'] = {
                            'manufacturer': board.Manufacturer or 'Unknown',
                            'product': board.Product or 'Unknown',
                            'serial': board.SerialNumber or 'N/A'
                        }

                    # Software: Windows Version
                    for os in iWbemServices.ExecQuery("SELECT Caption, Version, BuildNumber, OSArchitecture FROM Win32_OperatingSystem"):
                        software_details['os'] = {
                            'name': os.Caption or 'Unknown',
                            'version': os.Version or 'N/A',
                            'build': os.BuildNumber or 'N/A',
                            'architecture': os.OSArchitecture or 'N/A'
                        }

                    # Software: All Installed Software via Registry
                    software_list = []
                    reg_paths = [
                        r"Software\Microsoft\Windows\CurrentVersion\Uninstall",
                        r"Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
                    ]
                    iRegProv = dcom.CoCreateInstanceEx(wmi.CLSID_StdRegProv, wmi.IID_IWbemServices)
                    iRegProvServices = iRegProv.NTLMLogin('//./root/default', NULL, NULL)

                    for path in reg_paths:
                        subkeys = iRegProvServices.ExecMethod('StdRegProv', 'EnumKey', hDefKey=0x80000002, sSubKeyName=path)
                        if subkeys.sNames:
                            for subkey in subkeys.sNames:
                                key_path = f"{path}\\{subkey}"
                                display_name = iRegProvServices.ExecMethod(
                                    'StdRegProv', 'GetStringValue',
                                    hDefKey=0x80000002, sSubKeyName=key_path, sValueName='DisplayName'
                                ).sValue
                                version = iRegProvServices.ExecMethod(
                                    'StdRegProv', 'GetStringValue',
                                    hDefKey=0x80000002, sSubKeyName=key_path, sValueName='DisplayVersion'
                                ).sValue
                                publisher = iRegProvServices.ExecMethod(
                                    'StdRegProv', 'GetStringValue',
                                    hDefKey=0x80000002, sSubKeyName=key_path, sValueName='Publisher'
                                ).sValue
                                install_date = iRegProvServices.ExecMethod(
                                    'StdRegProv', 'GetStringValue',
                                    hDefKey=0x80000002, sSubKeyName=key_path, sValueName='InstallDate'
                                ).sValue

                                if display_name:
                                    software_list.append({
                                        'name': display_name,
                                        'version': version or 'N/A',
                                        'vendor': publisher or 'N/A',
                                        'install_date': install_date or 'N/A'
                                    })

                    software_details['installed_software'] = software_list

                    # Cleanup
                    if iRegProvServices:
                        iRegProvServices.RemRelease()
                    if iWbemServices:
                        iWbemServices.RemRelease()
                    if dcom:
                        dcom.disconnect()

                    # Store in session
                    request.session['scan_result'] = {
                        'netbios_name': netbios_name,
                        'ipv4_address': target_ip,
                        'hardware_details': hardware_details,
                        'software_details': software_details
                    }

                    return render(request, 'scan_hardware/result.html', {
                        'netbios_name': netbios_name,
                        'ipv4_address': target_ip,
                        'hardware_details': hardware_details,
                        'software_details': software_details
                    })

                except Exception as e:
                    logger.error(f"Scan failed for {target_ip}: {str(e)}")
                    messages.error(request, f"Scan failed: {str(e)}")
                    if iRegProvServices:
                        iRegProvServices.RemRelease()
                    if iWbemServices:
                        iWbemServices.RemRelease()
                    if dcom:
                        dcom.disconnect()
                    return render(request, 'scan_hardware/scan.html')

            elif action == 'save':
                scan_result = request.session.get('scan_result')
                if not scan_result:
                    messages.error(request, "No scan results to save.")
                    return redirect('scan_hardware:scan')

                ScanRecord.objects.create(
                    netbios_name=scan_result['netbios_name'],
                    ipv4_address=scan_result['ipv4_address'],
                    hardware_details=scan_result['hardware_details'],
                    software_details=scan_result['software_details']
                )
                messages.success(request, "Scan results saved successfully.")
                del request.session['scan_result']
                return redirect('scan_hardware:scan')

            elif action == 'cancel':
                if 'scan_result' in request.session:
                    del request.session['scan_result']
                messages.info(request, "Scan results discarded.")
                return redirect('scan_hardware:scan')

    return render(request, 'scan_hardware/scan.html')
