from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    # Complaint list and create
    path('', views.complaint_list, name='complaint_list'),
    path('create/', views.complaint_create, name='complaint_create'),
    
    # Complaint detail, update, delete
    path('<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    path('<int:complaint_id>/edit/', views.complaint_update, name='complaint_update'),
    path('<int:complaint_id>/delete/', views.complaint_delete, name='complaint_delete'),
    
    # Phase 5: Replies and attachments
    path('<int:complaint_id>/reply/', views.add_reply, name='add_reply'),
    path('<int:complaint_id>/upload-attachment/', views.upload_attachment, name='upload_attachment'),
]
