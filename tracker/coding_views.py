import sys
import io
import json
import traceback
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CodingQuestion, CodingAttempt

@login_required
def coding_practice_view(request):
    if 'coding_questions' not in request.session:
        # Get 3 random coding questions
        questions = list(CodingQuestion.objects.all())
        random.shuffle(questions)
        request.session['coding_questions'] = [q.id for q in questions[:3]]
        request.session['coding_current_index'] = 0
        request.session['coding_score'] = 0
        request.session['coding_results'] = {}

    questions_ids = request.session.get('coding_questions', [])
    current_index = request.session.get('coding_current_index', 0)

    # If no questions in DB, create a dummy one
    if not questions_ids:
        dummy_q = CodingQuestion.objects.create(
            title="Determine the float floor",
            description="Determine the integer floor of the sum of two floating point numbers. The floor is the truncated float value, i.e. anything after the decimal point is dropped. For instance, floor(1.1 + 3.05) = floor(4.15) = 4.",
            constraints="0.1 < a, b < 10^6\na and b have at most 8 places after the decimal",
            initial_code="def addNumbers(a, b):\n    # Write your code here\n    pass",
            test_cases_json=json.dumps([{"input": [1.1, 3.05], "expected": 4}, {"input": [2.3, 4.1], "expected": 6}]),
            tag="Algorithms"
        )
        request.session['coding_questions'] = [dummy_q.id]
        questions_ids = [dummy_q.id]

    if current_index >= len(questions_ids):
        return redirect('coding_result')

    question = get_object_or_404(CodingQuestion, id=questions_ids[current_index])

    return render(request, "coding_practice.html", {
        "question": question,
        "current_index": current_index + 1,
        "total": len(questions_ids),
        "total_range": range(1, len(questions_ids) + 1)
    })

@csrf_exempt
@login_required
def coding_execute_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("code", "")
            question_id = data.get("question_id")
            
            question = get_object_or_404(CodingQuestion, id=question_id)
            test_cases = json.loads(question.test_cases_json)
            
            # Very basic and insecure execution for demonstration
            local_env = {}
            try:
                exec(code, {}, local_env)
            except Exception as e:
                return JsonResponse({"status": "error", "message": f"Syntax/Compile Error:\n{traceback.format_exc()}"})
            
            func_name = None
            for key in local_env:
                if callable(local_env[key]) and not key.startswith("__"):
                    func_name = key
                    break
            
            if not func_name:
                return JsonResponse({"status": "error", "message": "No function defined."})
                
            passed = 0
            total = len(test_cases)
            results = []
            
            for tc in test_cases:
                inputs = tc.get("input", [])
                expected = tc.get("expected")
                
                try:
                    res = local_env[func_name](*inputs)
                    if str(res) == str(expected) or type(expected)(res) == expected:
                        passed += 1
                        results.append({"status": "passed", "input": inputs, "expected": expected, "got": res})
                    else:
                        results.append({"status": "failed", "input": inputs, "expected": expected, "got": res})
                except Exception as e:
                    results.append({"status": "error", "message": str(e)})
            
            if passed == total:
                # Update score
                request.session['coding_score'] = request.session.get('coding_score', 0) + 10
                request.session['coding_current_index'] = request.session.get('coding_current_index', 0) + 1
                request.session.modified = True
                
                res_dict = request.session.get('coding_results', {})
                res_dict[question.tag] = res_dict.get(question.tag, 0) + 10
                request.session['coding_results'] = res_dict
                
                return JsonResponse({"status": "success", "message": "All test cases passed!", "redirect": True})
            else:
                return JsonResponse({"status": "partial", "passed": passed, "total": total, "results": results})
                
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
            
    return JsonResponse({"status": "invalid request"})

@login_required
def coding_result_view(request):
    score = request.session.get('coding_score', 0)
    questions = request.session.get('coding_questions', [])
    results_breakdown = request.session.get('coding_results', {})
    total_score = len(questions) * 10
    
    # Save attempt
    if questions:
        CodingAttempt.objects.create(
            user=request.user,
            score=score,
            total_questions=len(questions),
            tags_breakdown_json=json.dumps(results_breakdown)
        )
    
    # Clear session
    if 'coding_questions' in request.session:
        del request.session['coding_questions']
    if 'coding_current_index' in request.session:
        del request.session['coding_current_index']
    if 'coding_score' in request.session:
        del request.session['coding_score']
    if 'coding_results' in request.session:
        del request.session['coding_results']
        
    return render(request, "coding_result.html", {
        "score": score,
        "total": total_score,
        "breakdown": results_breakdown
    })
