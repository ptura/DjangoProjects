from decimal import Decimal

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_number', models.CharField(max_length=30, unique=True)),
                ('first_name', models.CharField(max_length=80)),
                ('last_name', models.CharField(max_length=80)),
                ('class_name', models.CharField(default='Class 1', max_length=80)),
                ('email', models.EmailField(blank=True, max_length=254)),
            ],
            options={'ordering': ['last_name', 'first_name']},
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assessment', models.CharField(default='Term 1', max_length=100)),
                ('score', models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(Decimal('0'))])),
                ('out_of', models.DecimalField(decimal_places=2, default=Decimal('100'), max_digits=7, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))])),
                ('recorded_at', models.DateField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='Blog.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='marks', to='Blog.subject')),
            ],
            options={'ordering': ['-recorded_at', 'student__last_name']},
        ),
        migrations.AddConstraint(
            model_name='mark',
            constraint=models.UniqueConstraint(fields=('student', 'subject', 'assessment'), name='unique_student_subject_assessment'),
        ),
        migrations.AddConstraint(
            model_name='mark',
            constraint=models.CheckConstraint(condition=models.Q(('score__lte', models.F('out_of'))), name='mark_score_not_over_max'),
        ),
    ]
