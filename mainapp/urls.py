from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.main),
    path('transfer', views.transfer),
    path('test', views.test),
    path('success', views.success),
]
