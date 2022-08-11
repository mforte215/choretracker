
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index, name='index'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('new-task/', views.CreateTaskView, name='new-task'),
    path('delete-task/<uuid:uuid>/', views.DeleteTaskView, name='delete-task'),
    path('index/sort/<str:orderby>/<str:direction>/', views.SortTableView, name='sort-table'),
]
