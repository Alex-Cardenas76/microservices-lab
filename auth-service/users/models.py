from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Crea y guarda un usuario con el email y contraseña proporcionados.
        """
        if not email:
            raise ValueError("El campo email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Crea y guarda un superusuario.
        """
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No se requiere ningún otro campo

    objects = UserManager()

    def __str__(self):
        return self.email

    # Permisos básicos para el panel de admin
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
