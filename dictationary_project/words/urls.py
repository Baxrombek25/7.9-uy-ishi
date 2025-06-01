from django.urls import path
from . import views

urlpatterns = [
    path('words/', views.word_list, name='word_list'),
    path('word/<int:pk>/', views.word_detail, name='word_detail'),
    path('categories/', views.category_list, name='category_list'),
]