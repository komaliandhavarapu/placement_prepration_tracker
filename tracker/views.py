from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Registration successful. Please login.")
        return redirect("login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")

from django.contrib.auth.decorators import login_required
from .models import Section


@login_required
def dashboard_view(request):
    sections = Section.objects.all()
    return render(request, "dashboard.html", {"sections": sections})

from .models import PracticeQuestion, Section, Progress

def practice_view(request, section_id):
    section = Section.objects.get(id=section_id)
    questions = PracticeQuestion.objects.filter(section=section)

    score = 0
    total = questions.count()
    submitted = False

    if request.method == "POST":
        submitted = True

        for q in questions:
            selected = request.POST.get(f"q{q.id}")
            if selected == q.correct_answer:
                score += 1

        # ✅ THIS IS THE IMPORTANT PART YOU ASKED ABOUT
        Progress.objects.create(
            user=request.user,
            section=section,
            attempted=total,
            correct=score
        )

    return render(
        request,
        "practice.html",
        {
            "section": section,
            "questions": questions,
            "score": score,
            "total": total,
            "submitted": submitted
        }
    )
