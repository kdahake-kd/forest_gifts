from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
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
import datetime
import razorpay
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

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



# Tree plans
from django.shortcuts import render, redirect
from .models import Tree, TreePlan
from django.contrib.auth.decorators import login_required

@login_required
def buy_one_tree(request):
    # Handle the logic for purchasing 1 tree
    return purchase_tree_plan(request, 4)

@login_required
def buy_five_trees(request):
    # Handle the logic for purchasing 5 trees
    return purchase_tree_plan(request, 5)

@login_required
def buy_ten_trees(request):
    # Handle the logic for purchasing 10 trees
    return purchase_tree_plan(request, 6)

# def purchase_tree_plan(request, number_of_trees):
#     plan = TreePlan.objects.get(number_of_trees=number_of_trees)
#     # Integrate your payment gateway here
#     # After successful payment
#     if payment_successful:
#         Tree.objects.create(user=request.user, name='Tree Plan', number_of_trees=number_of_trees, date_planted=date.today(), location='TBD')
#         # Update user's tree count in their profile or a related model
#         return redirect('user_section')  # Redirect to user profile or a confirmation page
#     else:
#         return render(request, 'payment_failed.html')  # Handle payment failure

from django.shortcuts import render, redirect, get_object_or_404
from .models import TreePlan, Tree
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings


# def purchase_tree_plan(request, plan_id):
#     plan = get_object_or_404(TreePlan, id=plan_id)
#     print(f"Plan ID: {plan.id}, Price: {plan.price}") 
#     # if request.method == 'POST':
#     # # Skip Razorpay and just simulate a successful payment
#     #     payment_successful = True
    
#     #     if payment_successful:
#     #     # Proceed with creating the Tree entry
#     #         print("payment successfull")
#     #         Tree.objects.create(
#     #         user=request.user,
#     #         tree_plan=plan,
#     #         name=f'{plan.number_of_trees} Tree(s) Plan',
#     #         number_of_trees=plan.number_of_trees,
#     #         date_planted=datetime.date.today(),
#     #         location='TBD'
#     #     )
#     #         return redirect('home')

#     if request.method == 'POST':
#         print("post method encounter")
#         # client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
#         client = razorpay.Client(auth=('rzp_test_PL6TC1CmHX0BfJ','django-insecure-tqse)&n6(-2++1mc!sq=2*4mo&%n2vi@ce(zhb##b8_e+@12ud' ))
        
#         # order_data = {
#         #     'amount': int(plan.price * 100),  # Amount in paise
#         #     'currency': 'INR',
#         #     'receipt': f'order_rcptid_{request.user.id}',
#         #     'payment_capture': '1'
#         # }
        
#         payment_data = {
#         'amount': plan.price,
#         'currency': 'INR',
#         'receipt': f'order_rcptid_{request.user.id}',
#         'payment_capture': '1'
#     }

#     # Create a Razorpay Order
#         order = client.order.create(data=payment_data)

#         return JsonResponse(order)
#         # try:
#         #     order = client.order.create(data=order_data)
#         #     order_id = order['id']
#         #     return render(request, 'payment_confirmation.html', {'order_id': order_id, 'plan': plan})
#         # except Exception as e:
#         #     print(f"Error creating Razorpay order: {e}")
#         #     return render(request, 'payment_failed.html')  # Redirect to a failure page

#     return render(request, 'purchase_tree_plan.html', {'plan': plan})




# @csrf_exempt
# def payment_success(request):
#     if request.method == "POST":
#         order_id = request.POST.get('order_id')
#         payment_id = request.POST.get('payment_id')

#         # TODO: Add additional logic to handle order confirmation, payment verification

#         # After confirming payment, create the Tree entry
#         plan = TreePlan.objects.get(id=request.session['plan_id'])
#         Tree.objects.create(
#             user=request.user,
#             tree_plan=plan,
#             name=f'{plan.number_of_trees} Tree(s) Plan',
#             number_of_trees=plan.number_of_trees,
#             date_planted=datetime.date.today(),
#             location='TBD'
#         )
#         return JsonResponse({'status': 'Payment successful'})
    
from django.http import JsonResponse
import json


# @csrf_exempt
# def payment_success(request):
    # if request.method == 'POST':
    #     data = json.loads(request.body)
        
    #     # Capture payment details from Razorpay response
    #     payment_id = data.get('payment_id')
    #     order_id = data.get('order_id')
    #     signature = data.get('signature')

    #     # You can verify the payment signature (optional but recommended)
    #     client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
    #     try:
    #         # Verify the Razorpay signature (for added security)
    #         params_dict = {
    #             'razorpay_order_id': order_id,
    #             'razorpay_payment_id': payment_id,
    #             'razorpay_signature': signature
    #         }
    #         client.utility.verify_payment_signature(params_dict)

    #         # Handle successful payment (e.g., update order, save tree data, etc.)
    #         print(f"Payment successful: {payment_id}")

    #         plan = TreePlan.objects.get(id=request.session['plan_id'])
    #         Tree.objects.create(
    #         user=request.user,
    #         tree_plan=plan,
    #         name=f'{plan.number_of_trees} Tree(s) Plan',
    #         number_of_trees=plan.number_of_trees,
    #         date_planted=datetime.date.today(),
    #         location='TBD'
    #     )

    #         # Redirect to a success page
    #         return JsonResponse({'status': 'success'}, status=200)
        
    #     except razorpay.errors.SignatureVerificationError as e:
    #         # Handle signature verification failure
    #         print(f"Payment verification failed: {e}")
    #         return JsonResponse({'status': 'failed', 'error': str(e)}, status=400)

    # # Redirect to the success page
    # return redirect('success_page') 

@csrf_exempt
@login_required
def payment_success(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        payment_id = request.POST.get('payment_id')

        client = razorpay.Client(auth=('rzp_test_fpZTg3Ah6evW1p', 'DhWsXmNQjBLLGnVz0yhwqm4U'))
        
        try:
            response = client.payment.fetch(payment_id)
            print("Razorpay Payment Response:", response)  # Log the response for debugging

            if response['order_id'] == order_id and response['status'] == 'captured':
                # Payment successful
                return JsonResponse({'status': 'success'})
            else:
                print("Payment verification failed: Order ID or status mismatch.")
                return JsonResponse({'status': 'fail', 'reason': 'Payment verification failed'}, status=400)
        except Exception as e:
            print(f"Error verifying payment: {e}")
            return JsonResponse({'status': 'fail', 'reason': str(e)}, status=400)

    return JsonResponse({'status': 'fail'}, status=400)


from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.conf import settings
import razorpay
from .models import TreePlan

@csrf_exempt
@login_required
def purchase_tree_plan(request, plan_id):
    # Fetch the selected plan
    plan = get_object_or_404(TreePlan, id=plan_id)
    print(f"Plan ID: {plan.id}, Price: {plan.price}") 

    if request.method == 'POST':
        print("POST method encountered, preparing payment...")

        # Razorpay client initialization
        client = razorpay.Client(auth=('rzp_test_fpZTg3Ah6evW1p', 'DhWsXmNQjBLLGnVz0yhwqm4U'))
        
        # Payment data for Razorpay
        payment_data = {
            'amount': int(plan.price * 100),  # Price should be in paise (₹1 = 100 paise)
            'currency': 'INR',
            'receipt': f'order_rcptid_{request.user.id}',
            'payment_capture': '1'  # Automatically capture payment
        }
        
        try:
            # Create a Razorpay order
            order = client.order.create(data=payment_data)
            print(f"Order created successfully: {order}")

            # return render(request, 'confirm_payment.html', {
            #     'plan': plan,
            #     'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            #     'order_id': order['id'],
            # })
            
            # Return the order details to the frontend
            return JsonResponse({
                'order_id': order['id'],
                'amount': order['amount'],  # Amount in paise
                'currency': order['currency'],
                'plan_name': plan.name,
                'razorpay_key_id': settings.RAZORPAY_KEY_ID
            })
            # return render(request, 'confirm_payment.html', {
            #     'plan': plan,
            #     'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            #     'order_id': order['id'],
            # })
        
        except Exception as e:
            print(f"Error creating Razorpay order: {e}")
            return render(request, 'payment_failed.html')  # Handle errors and display failure page
    
    # For GET requests, render the purchase tree plan page
    return render(request, 'purchase_tree_plan.html', {'plan': plan})



