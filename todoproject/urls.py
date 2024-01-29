from django.contrib import admin
from django.urls import path

from todoapplication import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todo/', views.TodoView.as_view()),
]
