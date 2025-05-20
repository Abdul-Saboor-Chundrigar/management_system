from django.test import TestCase
from django.contrib.auth.models import User

class TwoFactorTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', password='test123')
        
    def test_2fa_required(self):
        # Login should redirect to 2FA verification
        response = self.client.post('/2fa/login/', {'username':'testuser', 'password':'test123'})
        self.assertRedirects(response, '/2fa/verify/')
        
    def test_admin_bypass(self):
        admin = User.objects.create_superuser('administrator', password='Ufone@2288')
        self.client.login(username='admin', password='Ufone@2288')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
