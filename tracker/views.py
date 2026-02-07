from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
import json
import random

from .models import (
    PracticeQuestion,
    Section,
    Progress,
    MockTestAttempt,
)
from .utils import extract_text_from_pdf, map_jd_to_sections, extract_relevant_sections


# -------------------- AUTH --------------------

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

        if user:
            login(request, user)
            return redirect("dashboard")

        messages.error(request, "Invalid credentials")
        return redirect("login")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# -------------------- DASHBOARD --------------------

@login_required
def dashboard_view(request):
    sections = Section.objects.all()

    last_7_days = timezone.now() - timedelta(days=7)
    progress_qs = Progress.objects.filter(
        user=request.user,
        created_at__gte=last_7_days
    ).order_by("created_at")

    accuracy_data = [p.accuracy for p in progress_qs]
    labels = [p.created_at.strftime("%d %b") for p in progress_qs]

    return render(request, "dashboard.html", {
        "sections": sections,
        "accuracy_data": json.dumps(accuracy_data),
        "labels": json.dumps(labels),
    })


# -------------------- PRACTICE --------------------

@login_required
def practice_view(request, section_id):
    section = Section.objects.get(id=section_id)
    questions = PracticeQuestion.objects.filter(section=section)

    score = 0
    total = questions.count()
    submitted = False
    answers = {}

    if request.method == "POST":
        submitted = True

        for q in questions:
            selected = request.POST.get(f"q{q.id}")
            answers[q.id] = selected

            if selected and selected.upper() == q.correct_answer.upper():
                score += 1

        accuracy = (score / total) * 100 if total > 0 else 0

        Progress.objects.create(
            user=request.user,
            score=score,
            total_questions=total,
            accuracy=accuracy
        )

    return render(request, "practice.html", {
        "section": section,
        "questions": questions,
        "score": score,
        "total": total,
        "submitted": submitted,
        "answers": answers,
    })


# -------------------- MOCK TEST --------------------

@login_required
def mock_test_view(request):

    if request.method == "GET":
        questions = list(PracticeQuestion.objects.all())
        random.shuffle(questions)
        questions = questions[:12]
        request.session["mock_q_ids"] = [q.id for q in questions]

    else:
        q_ids = request.session.get("mock_q_ids", [])
        questions = PracticeQuestion.objects.filter(id__in=q_ids)

    score = 0
    total = len(questions)
    submitted = False

    if request.method == "POST":
        submitted = True

        for q in questions:
            if request.POST.get(f"q{q.id}") == q.correct_answer:
                score += 1

        accuracy = (score / total) * 100 if total > 0 else 0

        Progress.objects.create(
            user=request.user,
            score=score,
            total_questions=total,
            accuracy=accuracy
        )

    return render(request, "mock_test.html", {
        "questions": questions,
        "score": score,
        "total": total,
        "submitted": submitted,
    })


# -------------------- JD UPLOAD --------------------

@login_required
def upload_jd_view(request):
    if request.method == "POST":
        pdf = request.FILES.get("jd_pdf")

        jd_text = extract_text_from_pdf(pdf)
        section_names = map_jd_to_sections(jd_text)

        sections = Section.objects.filter(name__in=section_names)
        request.session["jd_sections"] = list(sections.values_list("id", flat=True))
        request.session["jd_text"] = jd_text

        return render(request, "jd_result.html", {
            "sections": sections
        })

    return render(request, "upload_jd.html")


@login_required
def jd_mock_test_view(request):
    section_ids = request.session.get("jd_sections", [])

    questions = PracticeQuestion.objects.filter(
        section_id__in=section_ids
    ).order_by("?")[:12]

    score = 0
    submitted = False

    if request.method == "POST":
        submitted = True
        for q in questions:
            if request.POST.get(f"q{q.id}") == q.correct_answer:
                score += 1

    return render(request, "mock_test.html", {
        "questions": questions,
        "score": score,
        "total": len(questions),
        "submitted": submitted,
    })


def jd_result_view(request):
    jd_text = request.session.get("jd_text", "")
    section_names = extract_relevant_sections(jd_text)
    sections = Section.objects.filter(name__in=section_names)

    return render(request, "jd_result.html", {
        "sections": sections
    })
