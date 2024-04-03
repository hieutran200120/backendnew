from django.urls import path
from .views import GetNewView

urlpatterns = [
    path('', GetNewView.as_view(), name='get_new5'),
]