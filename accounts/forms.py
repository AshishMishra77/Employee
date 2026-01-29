from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from hcaptcha.fields import hCaptchaField


class LoginForm(AuthenticationForm):
    captcha = hCaptchaField()


class RegisterForm(UserCreationForm):
    captcha = hCaptchaField()
