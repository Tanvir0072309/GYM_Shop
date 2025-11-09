from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse




def home(request):
    return render(request, 'index.html')


def admin_signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not email or not password:
            messages.error(request, "All fields are required")
            return redirect('admin_signup')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('admin_signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('admin_signup')

        # Create superuser
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, "Superuser created successfully. Please sign in.")
            return redirect('admin_login')
        except Exception as e:
            messages.error(request, f"Error creating superuser: {str(e)}")
            return redirect('admin_signup')

    return render(request, 'admin_auth.html', {'form_type': 'signup'})


# Admin login view
def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # only staff/admin can login
            login(request, user)
            return redirect('/admin/')
        else:
            messages.error(request, "Invalid credentials or not an admin")
            return redirect('admin_login')
    return render(request, 'admin_auth.html', {'form_type': 'signin'})

# Admin logout view
def admin_logout_view(request):
    logout(request)
    return redirect('admin_login')




def admin_change_password_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        new_password = request.POST['new_password']
        try:
            user = User.objects.get(username=username, is_staff=True)
            user.password = make_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully. Please sign in.")
            return redirect('admin_login')
        except User.DoesNotExist:
            messages.error(request, "Admin not found")
            return redirect('admin_change_password')
    return render(request, 'admin_change_password.html')




# Get all admins
def get_admins(request):
    if request.method == "GET":
        admins = User.objects.filter(is_superuser=True).values("id", "username", "email", "password")
        return JsonResponse(list(admins), safe=False)

# Add new admin
@csrf_exempt
def add_admin(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return JsonResponse({"status": "error", "message": "All fields are required"})

        if User.objects.filter(username=username).exists():
            return JsonResponse({"status": "error", "message": "Username already exists"})
        if User.objects.filter(email=email).exists():
            return JsonResponse({"status": "error", "message": "Email already exists"})

        User.objects.create_superuser(username=username, email=email, password=password)
        return JsonResponse({"status": "success"})

# Update admin
@csrf_exempt
def update_admin(request, admin_id):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            user = User.objects.get(id=admin_id, is_superuser=True)
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Admin not found"})

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if username: user.username = username
        if email: user.email = email
        if password: user.set_password(password)
        user.save()

        return JsonResponse({"status": "success"})

# Delete admin
@csrf_exempt
def delete_admin(request, admin_id):
    if request.method == "DELETE":
        try:
            user = User.objects.get(id=admin_id, is_superuser=True)
            user.delete()
            return JsonResponse({"status": "success"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Admin not found"})

def admin_panel_page(request):
    return render(request, "admin_panel.html")


from django.shortcuts import render, get_object_or_404
from .models import Product

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})





