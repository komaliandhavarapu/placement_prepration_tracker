from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import MockTestAttempt


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
from .models import Section, Progress

@login_required(login_url='login')
def dashboard_view(request):

    # Fetch all sections
    sections = Section.objects.all()

    # Fetch progress only for logged-in user
    progress_qs = Progress.objects.filter(user=request.user).order_by("created_at")

    # Chart Data
    labels = [f"Attempt {i+1}" for i in range(len(progress_qs))]
    accuracy_data = [p.accuracy for p in progress_qs]

    return render(request, "dashboard.html", {
        "sections": sections,
        "labels": labels,
        "accuracy_data": accuracy_data
    })



from django.contrib.auth.decorators import login_required
from .models import PracticeQuestion, Section, Progress

@login_required
def practice_view(request, section_id):
    section = Section.objects.get(id=section_id)
    questions = PracticeQuestion.objects.filter(section=section)

    score = 0
    total = questions.count()
    submitted = False
    answers = {}  # store user's answers

    if request.method == "POST":
        submitted = True

        for q in questions:
            selected = request.POST.get(f"q{q.id}")
            answers[q.id] = selected

            if selected and selected.upper() == q.correct_answer.upper():
                score += 1

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
            "submitted": submitted,
            "answers": answers,   # 🔥 IMPORTANT
        }
    )


import random
from django.contrib.auth.decorators import login_required
from .models import PracticeQuestion

@login_required
def mock_test_view(request):
    questions = list(PracticeQuestion.objects.all())
    random.shuffle(questions)
    questions = questions[:12]  # 12 questions

    score = 0
    total = len(questions)
    submitted = False
    submitted_answers = {}

    from .models import Progress

    if request.method == "POST":
        score = 0
        for q in questions:
             selected = request.POST.get(f"q{q.id}")
             if selected == q.correct_answer:
                 score += 1

        accuracy = (score / total) * 100 if total > 0 else 0

        Progress.objects.create(
                user=request.user,
                score=score,
                total_questions=total,
                accuracy=accuracy
        )


        submitted = True


    return render(
        request,
        "mock_test.html",
        {
            "questions": questions,
            "score": score,
            "total": total,
            "submitted": submitted,
            "submitted_answers": submitted_answers,  # ✅ KEY FIX
        }
    )

from .utils import extract_text_from_pdf, map_jd_to_sections
from .models import Section

@login_required
def upload_jd_view(request):
    if request.method == "POST":
        pdf = request.FILES.get("jd_pdf")

        jd_text = extract_text_from_pdf(pdf)
        section_names = map_jd_to_sections(jd_text)

        sections = Section.objects.filter(name__in=section_names)

        request.session["jd_sections"] = list(sections.values_list("id", flat=True))

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
        "submitted": submitted
    })
from .utils import extract_relevant_sections
from .models import Section

def jd_result_view(request):
    jd_text = request.session.get("jd_text", "")

    section_names = extract_relevant_sections(jd_text)

    sections = Section.objects.filter(name__in=section_names)

    return render(request, "jd_result.html", {
        "sections": sections
    })

