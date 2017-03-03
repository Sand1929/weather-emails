from django.db import models

class City(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=2)

    def __str__(self):
        return "{}, {}".format(self.name, self.state)

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
