from django.shortcuts import render

# Create your views here.
from django.db.models import Q  # Import Q for complex queries
from django.contrib.auth import authenticate, login as auth_login
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required 

User = get_user_model()


class HomePageView(TemplateView):
    template_name = 'home.html'


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Individual, CollegeStudent, IndustryOrganization

# Individual User Plant View
@login_required(login_url='/login/')
def individual_plant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')
        
        if name and date_of_birth and address:
            # Save the data to the Individual model
            individual = Individual.objects.create(
                user=request.user,
                name=name,
                date_of_birth=date_of_birth,
                address=address
            )
            individual.save()
            messages.success(request, 'Tree planted successfully!')
            return redirect('/')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'individual.html')


# College Student Plant View
@login_required(login_url='/tree/login/')
def college_student_plant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')
        college = request.POST.get('college')
        
        if name and date_of_birth and address and college:
            # Save the data to the CollegeStudent model
            college_student = CollegeStudent.objects.create(
                user=request.user,
                name=name,
                date_of_birth=date_of_birth,
                address=address,
                college=college
            )
            college_student.save()
            messages.success(request, 'Tree planted successfully as a College Student!')
            return redirect('/tree/')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'college.html')


# Industry/Organization User Plant View
@login_required(login_url='login/')
def industry_organization_plant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')
        organization_name = request.POST.get('organization_name')
        
        if name and date_of_birth and address and organization_name:
            # Save the data to the IndustryOrganization model
            industry_user = IndustryOrganization.objects.create(
                user=request.user,
                name=name,
                date_of_birth=date_of_birth,
                address=address,
                organization_name=organization_name
            )
            industry_user.save()
            messages.success(request, 'Tree planted successfully as an Industry/Organization member!')
            return redirect('/')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'industry.html')



def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists() or User.objects.filter(mobile=mobile).exists():
            messages.error(request, "Email or Mobile number already exists.")
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, email=email, password=password, mobile=mobile)
        user.save()
        messages.success(request, "Account created successfully.")
        return redirect('login')

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        login_input = request.POST.get('login')
        password = request.POST.get('password')

        try:
            # Check if the input is either email or mobile number
            user = User.objects.get(Q(email=login_input) | Q(mobile=login_input))
        except User.DoesNotExist:
            print("Invalid login credentials.")
            messages.error(request, "Invalid login credentials.")
            return render(request, 'login.html')

        # Authenticate using username and password
        

        if user is not None:
            print("user enter the data",user)

            auth_login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')  # Redirect to home or dashboard
        else:
            messages.error(request, "Invalid password.")
            return render(request, 'login.html')

    return render(request, 'login.html')
def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('/tree/')


