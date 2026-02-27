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


from django.utils import timezone

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    accuracy = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.accuracy}%"


class JobDescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to="jds/")
    extracted_text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
from django.db import models
from django.contrib.auth.models import User

class MockTestAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    accuracy = models.FloatField()
    attempted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.accuracy}%"