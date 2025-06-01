from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def str(self):
        return self.name

class Word(models.Model):
    word = models.CharField(max_length=255)
    definition = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    synonyms = models.ManyToManyField('self', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.word