"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
# urls.py
from django.urls import path
from myapp import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    # path('dashboard/', views.dashboard_view, name='dashboard'),
    # path('',views.login_view, name='login'),
    # path('register',views.register_view, name='regiter'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('create_call/', views.create_call, name='create_call'),
    path('fetch_call_summary/', views.fetch_call_summary, name='fetch_call_summary'),
    path('fetch_call_analytics/', views.fetch_call_analytics, name='fetch_call_analytics'),
]
