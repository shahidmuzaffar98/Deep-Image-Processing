from django.urls import path
from . import views

app_name = "color"

urlpatterns = [
	path('', views.CreateColorView.as_view(), name = "new_c"),
	path('gallery/',views.ColorListView.as_view(),name='list_c'),
	path('<int:pk>/', views.ColorDetailView.as_view(), name='detail_c'),
]

