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
    InterviewAttempt,
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
from django.utils import timezone
from datetime import timedelta
from .models import Progress
import json
@login_required
def dashboard_view(request):
    sections = Section.objects.all()

    last_7_days = timezone.now() - timedelta(days=7)
    progress_qs = Progress.objects.filter(
        user=request.user,
        created_at__gte=last_7_days
    )

    labels = []
    accuracy_data = []
    marks_data = []

    weakest_section = None
    lowest_accuracy = 101

    for section in sections:
        section_progress = progress_qs.filter(section=section)
        if section_progress.exists():
            avg_accuracy = sum(p.accuracy for p in section_progress) / section_progress.count()
            total_score = sum(p.score for p in section_progress)

            labels.append(section.name)
            accuracy_data.append(round(avg_accuracy, 2))
            marks_data.append(total_score)

            if avg_accuracy < lowest_accuracy:
                lowest_accuracy = avg_accuracy
                weakest_section = section.name

    if weakest_section:
        suggestion = f"You need more practice in <span class=\"font-semibold text-white\">{weakest_section}</span>. Your accuracy was {round(lowest_accuracy, 1)}% in the last 7 days."
    else:
        suggestion = "Take some practice tests to get personalized insights and section-wise analytics!"

    overall_accuracy = round(sum(accuracy_data) / len(accuracy_data), 2) if accuracy_data else 0

    return render(request, "dashboard.html", {
        "accuracy_data": json.dumps(accuracy_data),
        "marks_data": json.dumps(marks_data),
        "labels": json.dumps(labels),
        "sections": sections,
        "suggestion": suggestion,
        "overall_accuracy": overall_accuracy
    })


# -------------------- PRACTICE --------------------

import random
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PracticeQuestion, Section

@login_required
def practice_view(request, section_id):

    section = get_object_or_404(Section, id=section_id)

    questions = list(PracticeQuestion.objects.filter(section=section))
    
    # Fallback to all questions if no specific questions exist for this section
    if not questions:
        questions = list(PracticeQuestion.objects.all())
        
    random.shuffle(questions)
    questions = questions[:10]

    score = 0
    total = len(questions)
    submitted = False

    if request.method == "POST":

        for q in questions:
            selected = request.POST.get(f"q{q.id}")
            if selected == q.correct_answer:
                score += 1

        accuracy = (score / total) * 100 if total > 0 else 0
        from .models import Progress
        Progress.objects.create(
            user=request.user,
            section=section,
            score=score,
            total_questions=total,
            accuracy=accuracy
        )

        submitted = True  # ✅ Show Score Only

    return render(request, "practice.html", {
        "section": section,
        "questions": questions,
        "score": score,
        "total": total,
        "submitted": submitted,
    })

# -------------------- MOCK TEST --------------------

import random
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import PracticeQuestion

@login_required
def mock_test_view(request):

    questions = list(PracticeQuestion.objects.all())
    random.shuffle(questions)
    questions = questions[:12]

    score = 0
    total = len(questions)
    submitted = False

    if request.method == "POST":

        for q in questions:
            selected = request.POST.get(f"q{q.id}")
            if selected == q.correct_answer:
                score += 1

        accuracy = (score / total) * 100 if total > 0 else 0
        from .models import MockTestAttempt
        MockTestAttempt.objects.create(
            user=request.user,
            score=score,
            total_questions=total,
            accuracy=accuracy
        )

        submitted = True   # ✅ Score will show

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

    if section_ids:
        questions = list(PracticeQuestion.objects.filter(section_id__in=section_ids))
    else:
        questions = list(PracticeQuestion.objects.all())
        
    random.shuffle(questions)
    questions = questions[:12]

    score = 0
    submitted = False

    if request.method == "POST":
        submitted = True
        for q in questions:
            if request.POST.get(f"q{q.id}") == q.correct_answer:
                score += 1
                
        accuracy = (score / len(questions)) * 100 if len(questions) > 0 else 0
        from .models import MockTestAttempt
        MockTestAttempt.objects.create(
            user=request.user,
            score=score,
            total_questions=len(questions),
            accuracy=accuracy
        )

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


# -------------------- MOCK INTERVIEW --------------------

@login_required
def mock_interview_view(request):
    preset_questions = [
        "What are your greatest strengths and weaknesses?",
        "Describe a challenging situation you faced and how you handled it.",
        "Why should we hire you?"
    ]

    if request.method == "POST":
        video_blob = request.FILES.get("video")
        
        # Generate dummy detailed feedback upon completion
        score = random.randint(70, 95)
        fluency = random.randint(65, 95)
        relevance = random.randint(70, 98)
        
        feedback = "Your answer structure is great, and you provided good examples. To improve, work on maintaining consistent eye contact with the camera and minimizing filler words. Ensure your points directly tie back to the specific skills required for the role."
        
        attempt = InterviewAttempt(
            user=request.user,
            score=score,
            fluency_score=fluency,
            relevance_score=relevance,
            overall_feedback=feedback,
        )
        if video_blob:
            attempt.video_recording.save(f"interview_{request.user.username}_{timezone.now().strftime('%Y%m%d%H%M%S')}.webm", video_blob)
        attempt.save()

        # Save ID to session to retrieve on the results page
        request.session['last_interview_id'] = attempt.id
        
        # Used for AJAX form submits
        from django.http import JsonResponse
        return JsonResponse({"status": "success", "redirect_url": "/mock-interview-result/"})

    return render(request, "mock_interview.html", {
        "questions": preset_questions
    })

@login_required
def mock_interview_result_view(request):
    attempt_id = request.session.get('last_interview_id')
    if not attempt_id:
        return redirect("dashboard")
        
    from django.shortcuts import get_object_or_404
    attempt = get_object_or_404(InterviewAttempt, id=attempt_id)
    
    return render(request, "mock_interview_result.html", {
        "attempt": attempt
    })
