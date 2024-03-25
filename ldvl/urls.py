from django.urls import path
from .views import APIViews
from .views import GetNewView

urlpatterns = [
    path('', APIViews.as_view(), name='api_data6'),
    path('get_new/', GetNewView.as_view(), name='get_new6'),
]