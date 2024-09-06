from django.urls import path
from .views import HomePageView
from tree import views


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('register',views.register,name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('individual/', views.individual_plant, name='individual'),
    path('college_student/', views.college_student_plant, name='college_student'),
    path('industry_organization/', views.industry_organization_plant, name='industry_organization'),
]