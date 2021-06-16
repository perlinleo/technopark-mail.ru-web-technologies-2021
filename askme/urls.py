
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('hot/', views.hot_questions, name='hot_questions'),
    path('tag/<str:name>/', views.tag_questions, name='tag_questions'),
    path('question/<int:pk>/', views.answers_for_question, name='answers_for_questions'),
    path('/login/', views.login, name='login'),
    path('votes/', views.votes, name='votes'),
     path('/logout/', views.logout, name='logout'),
     path(' ask/login/', views.login, name='login'),
    path('/signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
    path('settings/', views.settings, name='settings'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


url('/ask/account/', admin.site.urls)
url('ask/', admin.site.urls)