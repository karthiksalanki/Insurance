from django.urls import path
from .views import *

urlpatterns = [
    path('policies/', policies, name='list_or_create_policies'),
    path('policy/<int:policy_id>/', policy, name='get_or_update_policy'),
    path('comments/<int:policy_id>/', comments, name="list_or_create_comments"),
]
