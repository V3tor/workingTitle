from django.db import models

# Create your models here.

class Actor(models.Model):
	id = models.IntegerField(primary_key=True,unique=True)
	fname = models.CharField(max_length=100)
	lname = models.CharField(max_length=100)
	bdate = models.DateField()
	blocation = models.CharField(max_length=100)
	bio = models.TextField()

class Director(models.Model):
	id = models.IntegerField(primary_key=True,unique=True)
	fname = models.CharField(max_length=100)
	lname = models.CharField(max_length=100)

class Genre(models.Model):
	id = models.IntegerField(primary_key=True,unique=True)
	name = models.CharField(max_length=100)

class Rating(models.Model):
	id = models.IntegerField(primary_key=True,unique=True)
	name = models.CharField(max_length=100)

class PlotKeywords(models.Model):
	id = models.IntegerField(primary_key=True,unique=True)
	key = models.CharField(max_length=100)

class Movie(models.Model):
	id = models.IntegerField(primary_key=True,unique=True)
	title = models.CharField(max_length=100)
	runtime = models.IntegerField()
	release_date = models.DateField()
	genre = models.ForeignKey(Genre)
	rating = models.ForeignKey(Rating)
	description = models.TextField()
	director = models.ForeignKey(Director)
	plotKeywords = models.ForeignKey(PlotKeywords)
	




	


