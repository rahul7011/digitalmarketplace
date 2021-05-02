from django.db import models
from django.shortcuts import redirect, reverse

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

    def get_absolute_url(self):
        return reverse("books:book-detail", kwargs={
            "slug": self.slug
        })


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter_number = models.IntegerField()
    title = models.CharField(max_length=80)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("books:chapter-detail", kwargs={
        "book_slug": self.book.slug,
        "chapter_number":self.chapter_number,
        })


class Exercise(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    exercise_number = models.IntegerField()
    page_number = models.IntegerField()
    title = models.CharField(max_length=80)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("books:exercise-detail", kwargs={
            "book_slug": self.chapter.book.slug,
            "chapter_number":self.chapter.chapter_number,
            "exercise_number":self.exercise_number
        })
    
class Solution(models.Model):
    excercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    solution_number = models.IntegerField()
    image = models.ImageField()


    def __str__(self):
        return f"{self.excercise}-{self.pk}"
