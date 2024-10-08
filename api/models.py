from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

def upload_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.userProfile.id)+str(instance.nickName)+str(".")+str(ext)])

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('email is must')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using= self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
class Dictionary(models.Model):
    text = models.TextField(max_length=20)



class Post(models.Model):
    userPost = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userPost',
        on_delete=models.CASCADE
    )
    main = models.TextField(max_length=150)
    booktitle = models.TextField(max_length=80)
    author = models.TextField(max_length=40)
    sub = models.TextField(max_length=800)
    created_on = models.DateTimeField(auto_now_add=True)
    good = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='good',blank=True)
    word = models.ManyToManyField(Dictionary, related_name='word',blank=True)

    def __str__(self):
        return self.main


class Profile(models.Model):
    nickName = models.TextField(max_length=20)
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userProfile',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)
    download = models.ManyToManyField(Post,related_name='download',blank=True)

    def __str__(self):
        return self.nickName

class SearchInfo(models.Model):
    user = models.ManyToManyField(Profile, related_name='searchUser',blank=True)
    count = models.PositiveSmallIntegerField(default=0)
    text = models.ManyToManyField(Dictionary, related_name='searchText',blank=True)
    searched_on = models.DateTimeField(auto_now=True)



class Comment(models.Model):
    text = models.TextField(max_length=200)
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userComment',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


    











