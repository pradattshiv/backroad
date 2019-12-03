from django.db import models


class csv_data(models.Model):
    SSname = models.CharField(max_length=50)
    Route = models.IntegerField()
    District = models.CharField(max_length=50)
    Town = models.IntegerField()
    Day = models.IntegerField()
    Supervisor = models.CharField(max_length=30)
    VSR = models.CharField(max_length=30)
    Contact = models.IntegerField()
    month = models.CharField(max_length=30, blank=True)
    # def __str__(self):
    #     return self.SSname
    

class temp_ssdata(models.Model):
    SSname = models.CharField(max_length=50)
    Route = models.IntegerField()
    District = models.CharField(max_length=50)
    Town = models.IntegerField()
    Day = models.IntegerField()
    Supervisor = models.CharField(max_length=30)
    VSR = models.CharField(max_length=30)
    Contact = models.IntegerField()        
    month = models.CharField(max_length=30, blank=True)
    # def __str__(self):
    #     return self.SSname
    