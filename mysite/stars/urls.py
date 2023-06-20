from django.urls import path
from . import views
from django.views.generic import TemplateView

# https://docs.djangoproject.com/en/3.0/topics/http/urls/
app_name = 'stars'
urlpatterns = [
    path('', views.StarList.as_view(), name='all'), # Read
    path('main/create/', views.StarCreate.as_view(), name='star_create'), # Create
    path('main/<int:pk>/update/', views.StarUpdate.as_view(), name='star_update'), # Update
    path('main/<int:pk>/delete/', views.StarDelete.as_view(), name='star_delete'), # Delete
    path('lookup/', views.TypeView.as_view(), name='type_list'),
    path('lookup/create/', views.TypeCreate.as_view(), name='type_create'),
    path('lookup/<int:pk>/update/', views.TypeUpdate.as_view(), name='type_update'),
    path('lookup/<int:pk>/delete/', views.TypeDelete.as_view(), name='type_delete'),
]

# Note that make_ and auto_ give us uniqueness within this application