from django.db import models


# Create your models here.

class Users(models.Model):
    u_name = models.CharField(max_length=10)
    u_password = models.CharField(max_length=255)
    u_ticket = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.u_name

    class Meta:
        db_table = 'user'