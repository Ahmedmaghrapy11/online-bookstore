from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from .forms import CustomUserCreationForm
from .views import SignupPageView

# Create your tests here.
class CustomUserTests(TestCase):
    def test_create_user(self):
        _user = get_user_model()
        user = _user.objects.create_user(
            username = 'hesham',
            email = 'hesham@gmail.com',
            password = '123456'
        )
        self.assertEqual(user.username, 'hesham')
        self.assertEqual(user.email, 'hesham@gmail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        _user = get_user_model()
        admin_user = _user.objects.create_superuser(
            username = 'superuserhesham',
            email = 'superhesham@gmail.com',
            password = '123456'
        )
        self.assertEqual(admin_user.username, 'superuserhesham')
        self.assertEqual(admin_user.email, 'superhesham@gmail.com')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_superuser)

class SignupPageTests(TestCase):
    
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'signup.html')
        self.assertContains(self.response, 'Sign Up')
        self.assertNotContains(self.response, 'content does not exist')

    def test_signup_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEqual(view.func.__name__, SignupPageView.as_view().__name__)