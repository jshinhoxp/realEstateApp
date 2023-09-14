from django.db import models
# NOTE: Make sure to migrate after any changes on models

class House(models.Model):
	# Model Attributes
	address=models.CharField(max_length=30, default="2101 N Northlake Way")
	city=models.CharField(max_length=20, default="Seattle")
	state=models.CharField(max_length=2, default="WA")
	zipcode=models.IntegerField(default=98103)
	bedrooms=models.IntegerField(default=3)
	bathrooms=models.IntegerField(default=2)
	sqft_living=models.IntegerField(default=2000)
	sqft_lot=models.IntegerField(default=3500)
	floors=models.IntegerField(default=1)
	# Processed Attributes
	fullAddress=models.CharField(max_length=50, default='UNK')
	latitude=models.FloatField(default=0)
	longitude=models.FloatField(default=0)
	estPrice=models.IntegerField(default=0)
	created = models.DateTimeField(auto_now_add=True)
	

	# Display string
	def __str__(self):
		return '{}'.format(self.fullAddress)
	