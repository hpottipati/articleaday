"""blindsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import homepage.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage.views.home, name='home'),
    path('upload', homepage.views.getProfession, name='upload'),
    path('prediction/', homepage.views.prediction, name='prediction'),
    path('register/', homepage.views.registerPage, name='register'),
    path('login/', homepage.views.loginPage, name='login'),
    path('logout/', homepage.views.logoutUser, name='logout'),
    path('aboutus/', homepage.views.aboutUsPage, name='aboutus'),
    path('autosorter/', homepage.views.autoSorterPage, name='autosorter'),
]
