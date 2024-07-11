import os
import django
import sys
import hashlib
from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import site
from django.apps import apps
from unittest import mock
from .models import Account, post_save_compress_img
from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm

# Set up Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'Fallstudie_Calendar.settings'
django.setup()

class AccountModelTests(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='password123'
        )

    def test_create_user(self):
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('password123'))
        self.assertFalse(self.user.is_admin)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        admin_user = self.user_model.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123'
        )
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.check_password('adminpass123'))
        self.assertTrue(admin_user.is_admin)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_upload_location(self):
        filename = 'test_image.jpg'
        upload_path = self.user.profile_image.field.upload_to(self.user, filename)
        expected_path = f'profile_images/{hashlib.md5(str(self.user.email).encode()).hexdigest()}.jpg'
        self.assertEqual(upload_path, expected_path)

    def test_post_save_compress_img(self):
        # This test needs to mock the image saving process
        with mock.patch('PIL.Image.open') as mock_open:
            instance = self.user
            instance.profile_image = 'path/to/image.jpg'
            post_save_compress_img(sender=self.user_model, instance=instance)
            mock_open.assert_called_once_with(instance.profile_image.path)
            mock_open().save.assert_called_once_with(instance.profile_image.path, optimize=True, quality=30)


class AccountViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='password123'
        )

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_logout_view(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        new_user = self.user_model.objects.get(email='newuser@example.com')
        self.assertIsNotNone(new_user)


class AccountFormsTests(TestCase):

    def test_registration_form_valid(self):
        form_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_invalid(self):
        form_data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'differentpassword'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_authentication_form_valid(self):
        user = get_user_model().objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='password123'
        )
        form_data = {
            'email': 'testuser@example.com',
            'password': 'password123'
        }
        form = AccountAuthenticationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_authentication_form_invalid(self):
        form_data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        form = AccountAuthenticationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_account_update_form(self):
        user = get_user_model().objects.create_user(
            email='testuser@example.com',
            username='testuser',
            password='password123'
        )
        form_data = {
            'email': 'updateduser@example.com',
            'username': 'updateduser',
            'password': 'password123'
        }
        form = AccountUpdateForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.email, 'updateduser@example.com')
        self.assertEqual(updated_user.username, 'updateduser')


class AccountAdminTests(TestCase):

    def test_account_model_registered(self):
        self.assertTrue(site.is_registered(Account))


class AccountAppConfigTests(TestCase):

    def test_apps_config(self):
        self.assertEqual(apps.get_app_config('account').name, 'account')
