from django.urls import path
from . import views
from django.views.generic import TemplateView

# https://docs.djangoproject.com/en/3.0/topics/http/urls/
app_name = 'pets'
urlpatterns = [
    path('', views.PetList.as_view(), name='all'), # Read
    path('main/create/', views.PetCreate.as_view(), name='pet_create'), # Create
    path('main/<int:pk>/update/', views.PetUpdate.as_view(), name='pet_update'), # Update
    path('main/<int:pk>/delete/', views.PetDelete.as_view(), name='pet_delete'), # Delete
    path('lookup/', views.TypeView.as_view(), name='type_list'),
    path('lookup/create/', views.TypeCreate.as_view(), name='type_create'),
    path('lookup/<int:pk>/update/', views.TypeUpdate.as_view(), name='type_update'),
    path('lookup/<int:pk>/delete/', views.TypeDelete.as_view(), name='type_delete'),
]

# Note that type_ and pet_ give us uniqueness within this application