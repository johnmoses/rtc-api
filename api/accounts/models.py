import pyotp
import base64
from django.db import models
from datetime import datetime
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from sms import send_sms
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

class generateKey:
    @staticmethod
    def returnValue():
        return str(datetime.date(datetime.now())) + "Key"

def _generate_code():
    keygen = generateKey()
    key = base64.b32encode(keygen.returnValue().encode())
    otp = pyotp.TOTP(key)
    return otp.now()


class UserManager(BaseUserManager):
    def _create_user(
            self, username, password,
            is_staff, is_admin, is_superuser, is_business, **extra_fields):

        now = timezone.now()
        if not username:
            raise ValueError('Users must have username')
        user = self.model(
            username=username,
            is_staff=is_staff, is_admin=is_admin, is_superuser=is_superuser, is_business=is_business,
            last_login=now, date_joined=now, **extra_fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(
            username, password, False, False, False, False, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(
            username, password, True, True, True, True, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    avatar = models.ImageField(default="default.jpg")
    mobile = models.CharField(max_length=15, null=True, blank=True, unique=True, default=None)
    email = models.EmailField(max_length=100, null=True, blank=True, unique=True, default=None)
    gender = models.CharField(max_length=5, null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=30, null=True, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_business = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'User'
        managed = True

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def sms_user(self, message, from_number, **kwargs):
        send_sms(subject, message, from_number, [self.mobile], **kwargs)

    def __str__(self):
        return self.username

class OTPCodeManager(models.Manager):
    def create_otp_code(self, user, ipaddr):
        code = _generate_code()
        otp_code = self.create(user=user, code=code, ipaddr=ipaddr)

        return otp_code

    def set_is_verified(self, code):
        try:
            otp_code = OTPCode.objects.get(code=code)
            otp_code.user.is_verified = True
            otp_code.user.save()
            return True
        except OTPCode.DoesNotExist:
            pass
        return False


class AbstractBaseCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    code = models.CharField(max_length=50, primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True

    def send_email(self):
        subject = 'Code'
        message = 'Your code is ' + self.code
        send_mail(subject, message, '', [self.user.email])

    def send_sms(self):
        message = 'Your code is ' + self.code
        send_sms(message, '', [self.user.mobile])

    def __str__(self):
        return self.code


class OTPCode(AbstractBaseCode):
    ipaddr = models.GenericIPAddressField()
    counter = models.IntegerField(default=0, blank=False) 

    objects = OTPCodeManager()

    def send_otp_email(self):
        self.send_email()

    def send_otp_sms(self):
        self.send_sms()
