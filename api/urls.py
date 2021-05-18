from django.urls import path, include
from . import views
from rest_framework import routers
from .views import LoginAPIView

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'department/list' , views.Departments)
#router.register(r'employee/list' , views.emp_list)

urlpatterns = [
    path('', include(router.urls) ),
    path('login/', LoginAPIView.as_view(), name='login'),

    path('employee/list', views.emp_list , name='emp-list'),
    path('employee/register', views.register, name='emp_register'),
    path('employee/update', views.update_details, name='emp_edit'),

    #path('department/list', views.add_department.as_view() , name='dept-list'),
    ]



