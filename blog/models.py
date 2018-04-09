from django.db import models
from django.contrib.auth.models import User

from hc.settings import SITE_ROOT

# Create your models here.
class Categorie(models.Model):
    name = models.CharField(max_length=30,null=True, blank=True)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=30, null=True, blank=True)
    author = models.OneToOneField(User,blank=True, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    body = models.TextField()
    

    def __str__(self):
        return self.title, self.id
    
    def url(self):
        return "/blog/%s" % str(self.title)