from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True, default=None)
    email = models.CharField(max_length=100, unique=True, default=None)
    password = models.CharField(default=None, max_length=255)
    id = models.AutoField(primary_key=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    is_anonymous = []
    is_authenticated = []
    objects = UserManager()


class Restaurant(models.Model):
    name = models.CharField(max_length=30, unique=True, default=None)
    address = models.CharField(max_length=30, unique=True, default=None)
    owner = models.CharField(max_length=20, unique=True, default=None)
    id = models.AutoField(primary_key=True)
    def __str__(self) -> str:
        return self.name
    
class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, null=True, blank=True, on_delete=models.CASCADE)
    menu = models.TextField(unique=True)
    def __str__(self):
        return self.menu
    objects = UserManager()

class Employee(models.Model):
    first_name = models.CharField(max_length=20, unique=True, default=None)
    last_name = models.CharField(max_length=20, unique=True, default=None)
    email = models.CharField(max_length=100, unique=True, default=None)
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    def __str__(self):
        return self.first_name + ' ' + self.last_name
SCORES = (
    (+1, "+1"),
    (-1, "-1"),
)
CHOICE = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)
class Vote(models.Model):
    day = models.IntegerField(choices=CHOICE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    vote = models.SmallIntegerField(choices=SCORES)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('employee', 'menu'),)
    def __str__(self):
        return f"{self.employee}: {self.vote} on {self.menu}"
    
    def is_upvote(self):
        return self.vote == 1

    def is_downvote(self):
        return self.vote == -1