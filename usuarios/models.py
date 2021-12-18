from django.db import models

# from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, BaseUserManager

# BaseUser 
class UsuarioManager(BaseUserManager):
    # usar nas migrate
    use_in_migrations = True

    # funcao criar um user
    def _create_user(self, email, password, **extra_fields):
        # se campo não receber email correto
        if not email:
            # retorna email obrigatorio
            raise ValueError('O e-mail é obrigatório')
        # atributos
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    # todo usuario criado será usuario comun  
    def create_user(self, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    # criar um superuser
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')

        return self._create_user(email, password, **extra_fields)


# CustomUsuario 
class CustomUsuario(AbstractUser):
    email = models.EmailField('E-mail', unique=True)
    fone = models.CharField('Telefone', max_length=15)
    is_staff = models.BooleanField('Membro da equipe', default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'fone']

    def __str__(self):
        return self.email

    # os objetos desse customusuario sao gerenciados pelo usuario manage
    # se nao expecificar object o django não reconhece a customizacao
    # e seta autentificação padrão do django.
    objects = UsuarioManager() 
