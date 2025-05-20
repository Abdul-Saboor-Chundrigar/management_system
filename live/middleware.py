import requests
from django.utils import timezone
from .models import UserLocation
import logging
from geopy.geocoders import Nominatim
from django.conf import settings
import socket

logger = logging.getLogger(__name__)

class LocationTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.geolocator = Nominatim(user_agent="your_app_name", timeout=3)
        
        # Predefined locations for special IPs
        self.special_ips = {
            '127.0.0.1': {
                'latitude': 24.8607,
                'longitude': 67.0011,
                'city': 'Karachi',
                'country': 'Pakistan',
                'nearby_landmark': 'Development Server'
            },
            '::1': {
                'latitude': 24.8607,
                'longitude': 67.0011,
                'city': 'Karachi',
                'country': 'Pakistan',
                'nearby_landmark': 'Local IPv6 Server'
            }
        }

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                ip = self._get_client_ip(request)
                
                # Check if IP is in our predefined list
                if ip in self.special_ips:
                    location_data = self.special_ips[ip]
                else:
                    location_data = self._get_ip_location(ip)
                    if not location_data:  # If API fails, try browser geolocation
                        location_data = self._get_browser_location(request)
                
                # Create record only if we have valid data
                if location_data and location_data['latitude'] != 0:
                    UserLocation.objects.create(
                        user=request.user,
                        ip=ip,
                        **location_data
                    )
                    
            except Exception as e:
                logger.error(f"Location error: {str(e)}")
        
        return self.get_response(request)

    def _get_ip_location(self, ip):
        """Get location from IP geolocation services"""
        try:
            # Try ip-api.com first
            response = requests.get(f'http://ip-api.com/json/{ip}?fields=status,country,city,lat,lon', timeout=3)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return self._format_location(
                        data['lat'],
                        data['lon'],
                        data.get('city'),
                        data.get('country')
                    )
            
            # Fallback to ipapi.co
            response = requests.get(f'https://ipapi.co/{ip}/json/', timeout=3)
            if response.status_code == 200:
                data = response.json()
                return self._format_location(
                    float(data.get('latitude', 0)),
                    float(data.get('longitude', 0)),
                    data.get('city'),
                    data.get('country_name')
                )
                
        except requests.RequestException as e:
            logger.warning(f"IP lookup failed: {str(e)}")
        
        return None

    def _format_location(self, lat, lon, city, country):
        """Format location data with reverse geocoding for landmark"""
        if lat == 0 and lon == 0:
            return None
            
        landmark = self._get_landmark(lat, lon)
        return {
            'latitude': lat,
            'longitude': lon,
            'city': city or 'Unknown',
            'country': country or 'Unknown',
            'nearby_landmark': landmark or 'Unknown'
        }

    def _get_landmark(self, lat, lon):
        """Get nearest landmark using reverse geocoding"""
        try:
            location = self.geolocator.reverse(f"{lat}, {lon}", exactly_one=True)
            if location:
                return location.address.split(',')[0]  # Get first part of address
        except Exception as e:
            logger.warning(f"Reverse geocode failed: {str(e)}")
        return None

    def _get_browser_location(self, request):
        """Extract location from browser geolocation if available"""
        if 'latitude' in request.POST and 'longitude' in request.POST:
            try:
                lat = float(request.POST['latitude'])
                lon = float(request.POST['longitude'])
                return self._format_location(lat, lon, None, None)
            except:
                pass
        return None

    def _get_client_ip(self, request):
        """Get the real client IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip or '0.0.0.0'

    def _format_location(self, lat, lon, city, country):
        """Ensure invalid coordinates don't get saved"""
        if lat == 0 and lon == 0:
            return None  # Prevent saving invalid locations
        
        return {
            'latitude': lat,
            'longitude': lon,
            'city': city or self._reverse_geocode_city(lat, lon),
            'country': country or self._reverse_geocode_country(lat, lon),
            'nearby_landmark': self._get_landmark(lat, lon)
        }
