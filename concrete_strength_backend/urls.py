
from django.contrib import admin
from django.urls import path, include
import api.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('make-prediction/', api.views.make_prediction)
]
