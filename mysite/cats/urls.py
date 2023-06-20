from django.urls import path
from . import views
from django.views.generic import TemplateView

# https://docs.djangoproject.com/en/3.0/topics/http/urls/
app_name = 'cats'
urlpatterns = [
    path('', views.MainView.as_view(), name='all'), #read
    path('main/create/', views.CatCreate.as_view(), name='cat_create'), #create
    path('main/<int:pk>/update/', views.CatUpdate.as_view(), name='cat_update'), # Update
    path('main/<int:pk>/delete/', views.CatDelete.as_view(), name='cat_delete'), # Delete
    path('lookup/', views.BreedView.as_view(), name='breed_list'),
    path('lookup/create/', views.BreedCreate.as_view(), name='breed_create'),
    path('lookup/<int:pk>/update/', views.BreedUpdate.as_view(), name='breed_update'),
    path('lookup/<int:pk>/delete/', views.BreedDelete.as_view(), name='breed_delete'),
]