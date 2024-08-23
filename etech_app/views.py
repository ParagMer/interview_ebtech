from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import JsonResponse
from .models import User, Product
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from etech_app.forms import ProductForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def get_refresh_token(user):
    token = RefreshToken.for_user(user)
    return {"access": str(token.access_token), "refresh": str(token)}

# class users_login(APIView):
#     permission_classes = (AllowAny,)

#     def post(self, request):
#         try:
#             error = {}
#             if not request.data:
#                 return JsonResponse({"message":"Data is required"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
#             if not request.data.get('email'):
#                 error['email'] = "These Field Is Required"
#             if not request.data.get('password'):
#                 error['password'] = "These Field Is Required"
#             if bool(error):
#                 return JsonResponse({"message":error}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                
#             email = request.data["email"]
#             password  =request.data["password"]
            
#             try:
#                 user = User.objects.get(email=email)
#                 if user.check_password(password):
#                     access_token = get_refresh_token(user)
#                     return JsonResponse({"message": "login Sucessful", "token": access_token})
#             except User.DoesNotExist:
#                 return JsonResponse({"message": "Email is not registered"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
#         except Exception as e:
#             print(e)

@csrf_exempt
def users_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email:
            return JsonResponse({"error": "Email is required"})
        if not password:
            return JsonResponse({"error": "Password is required"})
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"message": "Login Successful", "redirect_url": "/dashboard/"})
            else:
                return JsonResponse({"message": "Invalid Credentials"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except User.DoesNotExist:
            return JsonResponse({"message": "Email is not registered"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
    else:
        return render(request, "login.html")
    

@login_required
def dashboard(request):
    user_email = request.user.email
    return render(request, "dashboard.html", {"email": user_email})

@login_required
def product_api(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Product created successfully!"})
        else:
            return JsonResponse({"errors": form.errors}, status=400)
    else:
        products = Product.objects.all()
        form = ProductForm()
        return render(request, "product_form.html", {"form": form, "products": products})
