"""
URL configuration for mydjangoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

from mydjangoproject import views
from Blog import views as dashboard_views
from Blog.forms import StaffAuthenticationForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='registration/login.html', authentication_form=StaffAuthenticationForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', dashboard_views.dashboard, name='dashboard'),
    path('students/', dashboard_views.student_list, name='student_list'),
    path('students/add/', dashboard_views.student_create, name='student_create'),
    path('subjects/', dashboard_views.subject_list, name='subject_list'),
    path('marks/add/', dashboard_views.mark_create, name='mark_create'),
    path('results/', dashboard_views.results, name='results'),
    path('charts/', dashboard_views.charts, name='charts'),
    path('aboutus/',views.aboutus),
    path('courses/',views.course),
    path('courses/<int:courseID>',views.courseDetails),
    path('studentmarks/',views.studentMarks),
    path('studentmarks-json/', views.studentMarksJson),

    # Blog pages remain available separately from the student dashboard.
    path('blog/', include('Blog.urls')),
]
