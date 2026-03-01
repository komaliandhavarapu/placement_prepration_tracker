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
def coding_practice_view(request, question_id=None):
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

    # If no questions in DB, create dummy ones
    if not questions_ids:
        dummy_1 = CodingQuestion.objects.create(
            title="Two Sum",
            description='''Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\nYou may assume that each input would have **exactly one solution**, and you may not use the same element twice.\nYou can return the answer in any order.\n\n### Function Description\nComplete the `twoSum` function in the editor below. \n`twoSum` has the following parameter(s):\n- `int nums[n]`: an array of integers to search\n- `int target`: the target sum to find\n\n### Returns\n- `int[2]`: an array containing the indices of the two numbers.''',
            constraints='''- `2 <= nums.length <= 10^4`\n- `-10^9 <= nums[i] <= 10^9`\n- `-10^9 <= target <= 10^9`\n- **Only one valid answer exists.**''',
            initial_code="def twoSum(nums, target):\n    # Write your code here\n    pass",
            test_cases_json=json.dumps([
                {"input": [[2, 7, 11, 15], 9], "expected": [0, 1]}, 
                {"input": [[3, 2, 4], 6], "expected": [1, 2]},
                {"input": [[3, 3], 6], "expected": [0, 1]}
            ]),
            tag="Algorithms"
        )
        dummy_2 = CodingQuestion.objects.create(
            title="Palindrome Number",
            description='''Given an integer `x`, return `True` if `x` is a palindrome, and `False` otherwise.\n\nAn integer is a palindrome when it reads the same forward and backward.\nFor example, `121` is a palindrome while `123` is not.\n\n### Function Description\nComplete the `isPalindrome` function in the editor below.\n\n`isPalindrome` has the following parameter(s):\n- `int x`: An integer to evaluate\n\n### Returns\n- `bool`: `True` if palindrome, `False` otherwise.''',
            constraints='''- `-2^31 <= x <= 2^31 - 1`''',
            initial_code="def isPalindrome(x):\n    # Write your code here\n    pass",
            test_cases_json=json.dumps([
                {"input": [121], "expected": True},
                {"input": [-121], "expected": False},
                {"input": [10], "expected": False}
            ]),
            tag="Algorithms"
        )
        dummy_3 = CodingQuestion.objects.create(
            title="Valid Parentheses",
            description='''Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.\n\n### Function Description\nComplete the `isValid` function in the editor below.\n\n`isValid` has the following parameter(s):\n- `str s`: A string of bracket characters\n\n### Returns\n- `bool`: `True` if the string is valid, `False` otherwise.''',
            constraints='''- `1 <= s.length <= 10^4`\n- `s` consists of parentheses only `'()[]{}'`.''',
            initial_code="def isValid(s):\n    # Write your code here\n    pass",
            test_cases_json=json.dumps([
                {"input": ["()"], "expected": True},
                {"input": ["()[]{}"], "expected": True},
                {"input": ["(]"], "expected": False}
            ]),
            tag="Data Structures"
        )
        
        request.session['coding_questions'] = [dummy_1.id, dummy_2.id, dummy_3.id]
        questions_ids = [dummy_1.id, dummy_2.id, dummy_3.id]

    if current_index >= len(questions_ids):
        return redirect('coding_result')

    # If question_id is provided via URL, use it and update session index if possible
    if question_id:
        question = get_object_or_404(CodingQuestion, id=question_id)
        if question_id in questions_ids:
            current_index = questions_ids.index(question_id)
            request.session['coding_current_index'] = current_index
    else:
        question = get_object_or_404(CodingQuestion, id=questions_ids[current_index])

    # Parse test cases to extract examples for UI
    examples = []
    try:
        test_cases = json.loads(question.test_cases_json)
        # Grab up to 2 test cases to display as examples
        for i, tc in enumerate(test_cases[:2]):
            examples.append({
                "num": i + 1,
                "input": ", ".join([str(val) for val in tc.get('input', [])]),
                "expected": str(tc.get('expected', ''))
            })
    except:
        pass

    all_questions = CodingQuestion.objects.all()

    return render(request, "coding_practice.html", {
        "question": question,
        "current_index": current_index + 1,
        "total": len(questions_ids),
        "total_range": range(1, len(questions_ids) + 1),
        "examples": examples,
        "all_questions": all_questions
    })

@csrf_exempt
@login_required
def coding_execute_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("code", "")
            question_id = data.get("question_id")
            is_submit = data.get("is_submit", False)
            
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
            
            if passed == total or is_submit:
                # Calculate prorated score
                score_gained = int((passed / total) * 10) if total > 0 else 0
                
                # Update score
                request.session['coding_score'] = request.session.get('coding_score', 0) + score_gained
                request.session['coding_current_index'] = request.session.get('coding_current_index', 0) + 1
                request.session.modified = True
                
                res_dict = request.session.get('coding_results', {})
                res_dict[question.tag] = res_dict.get(question.tag, 0) + score_gained
                request.session['coding_results'] = res_dict
                
                status_msg = "All test cases passed!" if passed == total else f"Submitted. {passed}/{total} test cases passed."
                stat_type = "success" if passed == total else "submitted"
                
                return JsonResponse({"status": stat_type, "message": status_msg, "redirect": True, "passed": passed, "total": total, "results": results})
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
