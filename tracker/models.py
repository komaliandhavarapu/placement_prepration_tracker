from django.db import models
from django.contrib.auth.models import User


class Section(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PracticeQuestion(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)    
    question = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1)

    def __str__(self):
        return self.question[:50]


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    attempted = models.IntegerField()
    correct = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.section.name}"


