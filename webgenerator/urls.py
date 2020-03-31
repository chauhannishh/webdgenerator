"""webgenerator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,name="index"),
    path('website_render',views.website_render,name="website_render"),
    path('college/<str:college_id>/lp/', views.login_page,name="login_page"),
    path('college/<str:college_id>/lp/user_login', views.user_login,name="user_login"),   
    path('college/<str:college_id>/user_logout/', views.user_logout,name="user_logout"),   
    path('college/<str:college_id>/', views.college, name="college"),
    path('admin_user_login/', views.admin_user_login, name="admin_user_login"),
    path('admin_user_logout/', views.admin_user_logout, name="admin_user_logout"),
    path('admins/', views.admin_login_page, name="admin_login_page"),
    path("college/<str:college_id>/department/",views.getDepartment,name="department"),
    path("college/<str:college_id>/department/<str:dept_name>",views.getSubjects,name="subjects"),
    path("college/<str:college_id>/lp/forum/<str:forum_id>/", views.forums, name="forums"),
    path("generateSyllabusPDF/", views.generateSyllabusPDF, name="generate_syllabus_pdf")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)