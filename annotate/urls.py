from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('', login_required(root), name='annotation_api_info'), 
    path('annotations', login_required(annotations), name='annotation_list'), 
    path('annotations/<int:aid>/', login_required(get_annotation), name='annotation_get'),
    path('search', login_required(search), name='annotation_search'),
]