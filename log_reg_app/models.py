from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 5 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 5 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords does not match"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        # email must match user
        user_list_to_login = User.objects.filter(email= postData['login_email'])
        if len(user_list_to_login) == 0:
            errors['login_email'] = "No email found"
        else:
            if not bcrypt.checkpw(postData['login_password'].encode(), user_list_to_login[0].password.encode()):
                errors['login_password'] = "There was a password problem"
        return errors  


    
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()