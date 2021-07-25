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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
import homepage.views, social_app.views, articleaday.views, contactform.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage.views.home, name='home'),
    path('upload', articleaday.views.getProfession, name='upload'),
    path('prediction/', articleaday.views.prediction, name='prediction'),
    path('article/', homepage.views.article, name='article'),
    path('register/', social_app.views.registerPage, name='register'),
    path('login/', social_app.views.loginPage, name='login'),
    path('logout/', social_app.views.logoutUser, name='logout'),
    path('aboutus/', homepage.views.aboutUsPage, name='aboutus'),
    path('autosorter/', homepage.views.autoSorterPage, name='autosorter'),
    path('runSorter', homepage.views.autoSortermain, name='runSorter'),
    path('juice', TemplateView.as_view(template_name='social_app/index.html')), 
    path('accounts/', include('allauth.urls')),
    path('contactus/', contactform.views.contactForm, name='contact'),


 ]

# urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
