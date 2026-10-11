from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import MarkForm, StudentForm, SubjectForm
from .models import Mark, Student, Subject
from .models import Post


# Create your views here.
def index(request):
    blog_posts = Post.objects.all()
    return render(request, 'blog/index.html', {'blog_posts': blog_posts})


staff_required = user_passes_test(lambda user: user.is_staff, login_url='login')


def grade_for(average):
    if average >= 80:
        return 'A'
    if average >= 70:
        return 'B'
    if average >= 60:
        return 'C'
    if average >= 50:
        return 'D'
    return 'F'


def result_rows():
    rows = []
    students = Student.objects.prefetch_related('marks')
    for student in students:
        marks = list(student.marks.all())
        if not marks:
            continue
        total_score = sum((mark.score for mark in marks), Decimal('0'))
        total_possible = sum((mark.out_of for mark in marks), Decimal('0'))
        average = (sum((mark.percentage for mark in marks), Decimal('0')) / len(marks)).quantize(Decimal('0.01'))
        rows.append({
            'student': student,
            'total_score': total_score,
            'total_possible': total_possible,
            'average': average,
            'grade': grade_for(average),
            'mark_count': len(marks),
        })

    rows.sort(key=lambda row: (-row['average'], row['student'].last_name.lower(), row['student'].first_name.lower()))
    previous_average = None
    previous_position = None
    for index, row in enumerate(rows, start=1):
        if row['average'] != previous_average:
            previous_position = index
            previous_average = row['average']
        row['position'] = previous_position
    return rows


@staff_required
def dashboard(request):
    all_marks = list(Mark.objects.select_related('student', 'subject'))
    overall_average = (
        sum((mark.percentage for mark in all_marks), Decimal('0')) / len(all_marks)
        if all_marks else Decimal('0')
    ).quantize(Decimal('0.01'))
    results = result_rows()
    return render(request, 'students/dashboard.html', {
        'student_count': Student.objects.count(),
        'subject_count': Subject.objects.count(),
        'mark_count': len(all_marks),
        'overall_average': overall_average,
        'top_students': results[:5],
        'recent_marks': all_marks[:8],
    })


@staff_required
def student_list(request):
    students = Student.objects.annotate(mark_count=Count('marks'))
    return render(request, 'students/student_list.html', {'students': students})


@staff_required
@require_http_methods(['GET', 'POST'])
def student_create(request):
    form = StudentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        student = form.save()
        messages.success(request, f'{student.full_name} was added.')
        return redirect('student_list')
    return render(request, 'students/student_form.html', {'form': form, 'page_title': 'Add student'})


@staff_required
@require_http_methods(['GET', 'POST'])
def subject_list(request):
    form = SubjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        subject = form.save()
        messages.success(request, f'{subject.name} was added.')
        return redirect('subject_list')
    return render(request, 'students/subject_list.html', {
        'form': form,
        'subjects': Subject.objects.annotate(mark_count=Count('marks')),
    })


@staff_required
@require_http_methods(['GET', 'POST'])
def mark_create(request):
    form = MarkForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        mark = form.save()
        messages.success(request, f'Mark saved for {mark.student.full_name}.')
        return redirect('results')
    return render(request, 'students/mark_form.html', {
        'form': form,
        'page_title': 'Enter marks',
        'has_students': Student.objects.exists(),
        'has_subjects': Subject.objects.exists(),
    })


@staff_required
def results(request):
    return render(request, 'students/results.html', {'results': result_rows()})


@staff_required
def charts(request):
    subject_labels = []
    subject_averages = []
    for subject in Subject.objects.prefetch_related('marks'):
        marks = list(subject.marks.all())
        if marks:
            subject_labels.append(subject.name)
            subject_averages.append(float(
                (sum((mark.percentage for mark in marks), Decimal('0')) / len(marks)).quantize(Decimal('0.01'))
            ))

    top_students = result_rows()[:5]
    return render(request, 'students/charts.html', {
        'subject_labels': subject_labels,
        'subject_averages': subject_averages,
        'top_labels': [row['student'].full_name for row in top_students],
        'top_averages': [float(row['average']) for row in top_students],
    })
