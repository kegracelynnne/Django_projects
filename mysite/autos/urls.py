from django.urls import path
from . import views
from django.views.generic import TemplateView

# https://docs.djangoproject.com/en/3.0/topics/http/urls/
app_name = 'autos'
urlpatterns = [
    path('', views.MainView.as_view(), name='all'), # Read
    path('main/create/', views.AutoCreate.as_view(), name='auto_create'), # Create
    path('main/<int:pk>/update/', views.AutoUpdate.as_view(), name='auto_update'), # Update
    path('main/<int:pk>/delete/', views.AutoDelete.as_view(), name='auto_delete'), # Delete
    path('lookup/', views.MakeView.as_view(), name='make_list'),
    path('lookup/create/', views.MakeCreate.as_view(), name='make_create'),
    path('lookup/<int:pk>/update/', views.MakeUpdate.as_view(), name='make_update'),
    path('lookup/<int:pk>/delete/', views.MakeDelete.as_view(), name='make_delete'),
]

# Note that make_ and auto_ give us uniqueness within this application