"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from polls import views as polls_views

# 第二种url添加方式
# extra_patterns = [
#     path('', polls_views.index, name='index'),
#     path('<int:question_id>/', polls_views.detail, name='detail'),
#     path('<int:question_id>/results', polls_views.results, name='results'),
#     path('<int:question_id>/vote', polls_views.vote, name='vote'),
#
# ]

urlpatterns = [
    path('polls/', include('polls.urls')),
    # path('polls/', include(extra_patterns)),
    path('admin/', admin.site.urls),

]
