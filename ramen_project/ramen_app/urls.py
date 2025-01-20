from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'ramen_app'

urlpatterns = [
    path('', views.ramen_list, name='ramen_list'),
    path('shop/<int:shop_id>/', views.ramen_detail, name='ramen_detail'),
    path('shop/<int:shop_id>/review/', views.add_review, name='add_review'),
    path('shop/<int:shop_id>/like/', views.like_shop, name='like_shop'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),  # ここが重要
]
