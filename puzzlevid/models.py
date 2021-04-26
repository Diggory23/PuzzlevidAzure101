from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail

'''
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name=None, last_name=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.first_name = first_name
        user.last_name = last_name

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name=None, last_name=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.first_name = first_name
        user.last_name = last_name

        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        help_text = "To keep your organisation anonymous you can use a personal email address"
    )
    first_name = models.CharField(
        max_length = 30,
        verbose_name = "First Name",
        null=True,
        blank=True
    )
    last_name = models.CharField(
        max_length = 30,
        verbose_name = "Last Name",
        null=True,
        blank=True
    )
    address = models.CharField(
        max_length = 255
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'customer_type']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = 'User'
'''
# Create your models here.
class Usuario(models.Model):
    nombre = models.TextField()
    apellido = models.TextField()
    gameTag = models.TextField()
    birth =models.DateField()


class Session(models.Model):
    usuarioId =  models.ForeignKey("Usuario", on_delete=models.SET_NULL, null=True)
    inicioSesion = models.DateTimeField()
    terminoSesion =models.DateTimeField()
    aciertosQuim = models.IntegerField()
    aciertosMate = models.IntegerField()
    aciertosGeo = models.IntegerField()
    aciertosFis = models.IntegerField()
    aciertosHist = models.IntegerField()
    enemigosEliminados = models.IntegerField()

class Nivel(models.Model):
    numeroNivel = models.IntegerField()
    nombreNivel = models.TextField()

class Intento(models.Model):
    nivelId =  models.ForeignKey("Nivel", on_delete=models.SET_NULL, null=True)
    sessionId =  models.ForeignKey("Session", on_delete=models.SET_NULL, null=True)
    numeroIntento = models.IntegerField()
    exito = models.BooleanField()
