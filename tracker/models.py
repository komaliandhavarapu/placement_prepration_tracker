from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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

class MockTestAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    accuracy = models.FloatField()
    attempted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.accuracy}%"

class InterviewAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    fluency_score = models.IntegerField(default=0)
    relevance_score = models.IntegerField(default=0)
    overall_feedback = models.TextField(blank=True, null=True)
    video_recording = models.FileField(upload_to="interview_recordings/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Interview ({self.score}/100)"

class CodingQuestion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    constraints = models.TextField(blank=True)
    initial_code = models.TextField(default="def solution():\n    pass")
    test_cases_json = models.TextField(help_text="JSON list of test case dicts [{'input': '...', 'expected': '...'}]")
    tag = models.CharField(max_length=50, default="Algorithms")

    def __str__(self):
        return self.title

class CodingAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=5)
    time_taken_seconds = models.IntegerField(default=0)
    tags_breakdown_json = models.TextField(default="{}")
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Coding Attempt ({self.score})"
