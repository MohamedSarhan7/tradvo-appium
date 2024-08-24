from django.test import TestCase

# Create your tests here.
# main/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import activate
from django.contrib.auth.models import User
from .models import App
from .forms import AppForm
class TestLoginPage(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password'
        )
        activate('en')
        self.client = Client()

    def test_login_page_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password'
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_failure(self):
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_redirect_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('dashboard'))


class TestRegisterPage(TestCase):
    def setUp(self):
        self.client = Client()
        activate('en')
    def test_register_page_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'Str0ngP@ssw0rd123!',
            'password2': 'Str0ngP@ssw0rd123!'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_register_failure(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'password',
            'password2': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertEqual(get_user_model().objects.count(), 0)

    def test_redirect_authenticated_user(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            password='password'
        )
        self.client.force_login(user)
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, reverse('dashboard'))
        


class AllAppsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.app1 = App.objects.create(name='App1', uploaded_by=self.user)
        self.app2 = App.objects.create(name='App2', uploaded_by=self.user)
        self.app3 = App.objects.create(name='App3', uploaded_by=User.objects.create_user(username='otheruser', password='password'))
        activate('en')
    def test_all_apps_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apps/all-apps.html')
        self.assertIn('apps', response.context)
        self.assertEqual(list(response.context['apps']), [self.app1, self.app2])



class AppCreateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        activate('en')
    
    def test_create_app(self):
        response = self.client.post(reverse('create'), {
            'name': 'New App',
            'apk_file_path': 'path/to/file.apk',
        })
        self.assertEqual(response.status_code, 200)  



class AppDeleteViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.app = App.objects.create(name='App to Delete', uploaded_by=self.user)
        activate('en')

    def test_delete_app(self):
        response = self.client.post(reverse('app-delete', args=[self.app.pk]))
        self.assertEqual(response.status_code, 302)  
        self.assertFalse(App.objects.filter(pk=self.app.pk).exists())




class AppDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.app = App.objects.create(name='App Details', uploaded_by=self.user)
        activate('en')
    def test_detail_view(self):
        response = self.client.get(reverse('app-detail', args=[self.app.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'apps/view-app.html')
        self.assertIn('app', response.context)
        self.assertEqual(response.context['app'], self.app)

from unittest.mock import patch

class StartAppiumTestViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.app = App.objects.create(name='Test App', uploaded_by=self.user)
        activate('en')
    @patch('main.views.run_appium_test.delay')  # Mocking the task
    def test_start_appium_test(self, mock_run_appium_test):
        response = self.client.get(reverse('run_appium_test', args=[self.app.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Appium test started.')
        mock_run_appium_test.assert_called_once_with(self.app.pk)
