from django.db import models
from django.conf import settings
# Create your models here.


class Color(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE,null=True)
	grayimg = models.ImageField(upload_to='color/',blank=True,null=True)
	clrimg = models.ImageField(upload_to='color/',blank=True,null=True)
