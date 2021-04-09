from django.db import models

class clicked_photo(models.Model):
	date_time=models.DateTimeField(auto_now_add=True)
	photo_name=models.ImageField(upload_to='images/')
	def __str__(self):
		return str(self.date_time)