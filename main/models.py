from django.db import models

class clicked_photo(models.Model):
	date_time=models.DateTimeField(auto_now_add=True)
	photo_name=models.ImageField(upload_to='images/')
	def __str__(self):
		return str(self.date_time)
class last_location(models.Model):
	latitude=models.CharField(max_length=20)
	longitude=models.CharField(max_length=20)
	altitude=models.CharField(max_length=20)
	accuracy=models.CharField(max_length=20)
	vertical_accuracy=models.CharField(max_length=20)
	speed=models.CharField(max_length=20)
	elapsedMs=models.CharField(max_length=20)
	provider=models.CharField(max_length=20)
	date_time=models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return str(self.date_time)