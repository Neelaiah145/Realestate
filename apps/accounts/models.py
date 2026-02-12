from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", User.Role.SUPERUSER)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    class Role(models.TextChoices):
        SUPERUSER = "superuser", "Superuser"
        AGENT = "agent", "Agent"
        ASSOCIATE = "associate", "Associate"

 
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True,unique=True)
    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True,
        default="profile_images/user_img.png"
    )


    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.AGENT
    )
    
 
    parent_agent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="associates",
        limit_choices_to={"role": "agent"}
    )
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta:
            permissions = [
                ('view_dashboard',"Permisison for Dashboard(Menu)"),
                ('view_create_associate',"Permission for create_agent(Menu)"),
                
        ]    



class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)