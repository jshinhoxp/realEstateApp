from django.db import models
# NOTE: Make sure to migrate after any changes on models

class House(models.Model):
	# Model Attributes
	address=models.CharField(max_length=15)
	city=models.CharField(max_length=15)
	state=models.CharField(max_length=2)
	bathrooms=models.IntegerField(default=0)
	bedrooms=models.IntegerField(default=0)
	sqft=models.IntegerField(default=0)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '{}'.format(self.address)
