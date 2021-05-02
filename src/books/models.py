from django.db import models

# Create your models here.
'''
    # Model heirarchy
    Author 1
        Book
            Chapter 1
                Excercise 1
                    Question 1
                    Question 2
                    ...
                Excercise 2
                ...
            chapter 2
            ...
        Book 2
        ...
    Author 2
    ...
'''


class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    slug = models.SlugField()  # this will be for detail view of authors

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    author = models.ManyToManyField(Author)
    title = models.CharField(max_length=80)
    publication_date = models.DateTimeField()
    # International Standard Book Number for refrence max=16
    isbn = models.CharField(max_length=16)
    slug = models.SlugField()
    cover = models.ImageField()
    price = models.FloatField()

    def __str__(self):
        return self.title


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter_number = models.IntegerField()
    title = models.CharField(max_length=80)

    def __str__(self):
        return self.title


class Exercise(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    exercise_number = models.IntegerField()
    page_number = models.IntegerField()
    title = models.CharField(max_length=80)

    def __str__(self):
        return self.title
    
class Solution(models.Model):
    excercise=models.ForeignKey(Exercise,on_delete=models.CASCADE)
    image=models.ImageField()

    def __str__(self):
        return  f"{self.excercise}-{self.pk}"
    
