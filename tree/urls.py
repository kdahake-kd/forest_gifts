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
    path('plan/1/', views.buy_one_tree, name='buy_one_tree'),
    path('plan/22/', views.buy_five_trees, name='buy_five_trees'),
    path('plan/33/', views.buy_ten_trees, name='buy_ten_trees'),
     path('purchase/<int:plan_id>/', views.purchase_tree_plan, name='purchase_tree_plan'),
    path('payment-success/', views.payment_success, name='payment_success'),
]

