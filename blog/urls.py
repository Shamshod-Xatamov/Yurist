from django.urls import path
from . import views

urlpatterns = [
    # Ro'yxat
    path('', views.blog_list, name='blog_list'),

    # Ichki sahifa (Diqqat: uuid bo'lishi shart!)
    path('<uuid:post_uuid>/', views.blog_detail, name='blog_detail'),
    path('like/<uuid:post_uuid>/', views.like_post, name='like_post'),
]