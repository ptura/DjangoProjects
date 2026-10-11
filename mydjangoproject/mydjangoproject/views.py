from django.http import HttpResponse
from django.shortcuts import render

def aboutus(request):
    return HttpResponse('we are learning django')


def course(request):
    return HttpResponse('this is django courses')


def courseDetails(request, courseID):
    return HttpResponse(courseID)

def studentMarks(request):
    student_marks = {
        'name': ['John', 'Jane', 'Bob'],
        'reg_no': ['123', '456', '789'],
        'marks': [85, 90, 78]
    }
    student_marks = zip(student_marks['name'], student_marks['reg_no'], student_marks['marks'])
    return render(request, "studentmarks.html", {'student_marks': student_marks})  


def studentMarksJson(request):
    student_marks = [
        {'name': 'John', 'reg_no': '123', 'marks': 85},
        {'name': 'Jane', 'reg_no': '456', 'marks': 90},
        {'name': 'Bob', 'reg_no': '789', 'marks': 78},
    ]
    return render(request, 'studentmarks_json.html', {'student_marks': student_marks})
