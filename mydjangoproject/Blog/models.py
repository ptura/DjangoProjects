from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db.models import Q

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=100)

    def __str__(self):
        return f' title: {self.title}, content: {self.content}, date_posted: {self.date_posted}, author: {self.author}'


class Student(models.Model):
    student_number = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    class_name = models.CharField(max_length=80, default='Class 1')
    email = models.EmailField(blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.student_number} — {self.full_name}'


class Subject(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name='marks')
    assessment = models.CharField(max_length=100, default='Term 1')
    score = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    out_of = models.DecimalField(max_digits=7, decimal_places=2, default=Decimal('100'), validators=[MinValueValidator(Decimal('0.01'))])
    recorded_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at', 'student__last_name']
        constraints = [
            models.UniqueConstraint(fields=['student', 'subject', 'assessment'], name='unique_student_subject_assessment'),
            models.CheckConstraint(condition=Q(score__lte=models.F('out_of')), name='mark_score_not_over_max'),
        ]

    @property
    def percentage(self):
        return (self.score / self.out_of * Decimal('100')).quantize(Decimal('0.01'))

    def clean(self):
        super().clean()
        if self.score is not None and self.out_of is not None and self.score > self.out_of:
            raise ValidationError({'score': 'The mark cannot be greater than the maximum mark.'})

    def __str__(self):
        return f'{self.student} · {self.subject}: {self.score}/{self.out_of}'
