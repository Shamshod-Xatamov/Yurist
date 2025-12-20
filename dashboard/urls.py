from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('blog/new/', views.blog_create, name='blog_create'),
    path('blog/edit/<uuid:post_uuid>/', views.blog_edit, name='blog_edit'),
    path('blog/delete/<uuid:post_uuid>/', views.blog_delete, name='blog_delete'),
]