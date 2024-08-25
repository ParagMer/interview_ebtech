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
from django.core.paginator import Paginator


# ------------------------------------------------------------DRF PART----------------------------------------------------------
# def get_refresh_token(user):
#     token = RefreshToken.for_user(user)
#     return {"access": str(token.access_token), "refresh": str(token)}

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



# ------------------------------------------------------------DJANGO PART----------------------------------------------------------
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
                return JsonResponse({"message": "Login Successful", "redirect_url": "/index/"}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"message": "Invalid Credentials"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except User.DoesNotExist:
            return JsonResponse({"message": "Email is not registered"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
    else:
        return render(request, "login.html")
    

@login_required
def dashboard(request):
    # return render(request, "index.html")
    user_email = request.user.email
    return render(request, "index.html", {"email": user_email})

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
        form = ProductForm()
        return render(request, "side-menu-light-add-product.html", {"form": form})

@login_required
def productListing(request):
    if request.method == "GET":
        products = Product.objects.all()
        paginator = Paginator(products, 10)  # Show 10 products per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "side-menu-light-product-list.html", {"page_obj": page_obj})
