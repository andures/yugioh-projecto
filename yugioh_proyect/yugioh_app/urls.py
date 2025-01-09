from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cartas/', views.cartas_list, name='cartas_list'),
    path('decks/', views.decks_list, name='decks_list'),
    path('decks/<int:deck_id>/', views.deck_detail, name='deck_detail'),
    path('decks/create/', views.deck_create, name='deck_create'),
    path('decks/create/<int:deck_id>/', views.deck_create, name='deck_create'),
    path('decks/<int:deck_id>/delete/', views.deck_delete, name='deck_delete'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('comunity/', views.comunity, name='comunity'),
]