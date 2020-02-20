from django.db import models
from unixtimestampfield.fields import UnixTimeStampField
# Create your models here.
class Switch(models.Model):
	name = models.CharField(max_length=10)
	t1 = models.BooleanField()
	t2 = models.BooleanField()
	t3 = models.BooleanField()
	t4 = models.BooleanField()
	t5 = models.BooleanField()
	timestamp = UnixTimeStampField()
	created_at = models.DateTimeField(null=True)
	switch_status = models.IntegerField(null=True) 

