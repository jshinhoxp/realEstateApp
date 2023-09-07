from django.db import models

# Create your models here. 
# Make sure to migrate after any changes on models
class Approvals(models.Model):
	# Drop down menus
	address=models.CharField(max_length=15)
	bathrooms=models.IntegerField(default=0)
	bedrooms=models.IntegerField(default=0)
	sqft=models.IntegerField(default=0)

	def __str__(self):
		return '{}'.format(self.address)
