from django.db import models
from django.contrib.auth.models import User
import datetime as dt
# Create your models here.

class Graph_modal(models.Model):
    class Meta:
        db_table = 'graph_modal'

    user_id = models.CharField(max_length = 30,blank =True)
    user_name = models.CharField(max_length = 30,blank =True)
    user_first_name = models.CharField(max_length = 40,blank =True)
    user_last_name = models.CharField(max_length = 40,blank =True)
    user_email = models.EmailField(max_length = 40,blank =True)
    user_status = models.CharField(max_length = 30,blank =True)
    user_phone_number = models.CharField(max_length = 10,blank =True)

    def save_user(self):
        self.save()

    @classmethod
    def get_all_users(cls):
        users = cls.objects.all()
        return users

    @classmethod
    def get_user(cls, id):
        user = UserModel.objects.get(user_id=id)
        return user

    @classmethod
    def filter_by_id(cls, id):
        user = UserModel.objects.filter(user_id=id).first()
        return user

