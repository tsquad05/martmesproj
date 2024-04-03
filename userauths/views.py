from django.shortcuts import render,redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout
from userauths.models import User
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError
from .utils import send_confirmation_email, reset_password
from .models import UserToken
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from userauths.decorators import password_reset_cooldown_required
def register_view(request):
    form = UserRegisterForm(request.POST)
    if request.method == "POST" and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if form.is_valid():
            try:
                
                new_user = form.save(commit=False)  # Don't save the user yet
                new_user.email_verified = False
                new_user.save()

                # Send confirmation email
                send_confirmation_email(request, new_user)
                fullname = form.cleaned_data.get("full_name")
                
                new_user = authenticate(username=form.cleaned_data['email'],
                                        password=form.cleaned_data['password']
                )
                login(request, new_user)
       
                return JsonResponse({'success': True, 'message': f"Hey {fullname}, account created successfully"})
            
            except IntegrityError as e:
               
                form.add_error('email', 'This email address is already in use.')
        
        errors = form.errors.as_json()
        return JsonResponse({'success': False, 'errors': errors})

    return JsonResponse({'success': False, 'message': "Invalid request"})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:index")
    if request.method == "POST" and  request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'message': "Successfully logged in."})
            else:
                
                return JsonResponse({'success': False, 'message': "Incorrect email or password."})
        except User.DoesNotExist:
           
            return JsonResponse({'success': False, 'message': f"User does not exist"})


    return JsonResponse({'success': False, 'message': "Invalid request"})

def logout_view(request):
    logout(request)
    return redirect("core:index")

def email_confirmed(request):
    return render(request, "emails/email-confirmed.html")


def email_invalid(request):
    return render(request, "emails/email-invalid.html")

def password_reset_success(request):
    return render(request, "password/password-reset-success.html")

def send_password_reset(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        try:
            if user:
                reset_password(request, user)
                return JsonResponse({'success': True, 'message': "A password reset email has been sent to your email"})
            else:
                return JsonResponse({'success': False, 'message': "User with this email does not exist."})
        except Exception as e:
            print(e)
    else:
        return JsonResponse({'success': False, 'message': "Invalid request"})

def password_reset_form(request, token):
    try:
        user_token = UserToken.objects.get(token=token, token_type='password_reset', used=False)
    except UserToken.DoesNotExist:
            # Token not found or already used
            return redirect('userauths:invalid_token')
    return render(request, 'password/password_reset_form.html', {'token': token})

def process_password_reset(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        password = request.POST.get('password')
        
        try:
            user_token = UserToken.objects.get(token=token, token_type='password_reset', used=False)
        except UserToken.DoesNotExist:
            # Token not found or already used
            return redirect('userauths:invalid_token')
        
        # Check if the token has expired
        if user_token.expires_at < timezone.now():
            # Token has expired
            return redirect('userauths:invalid_token')
        
        # Mark the token as used
        user_token.used = True
        user_token.save()
        
        # Update the user's password
        user = user_token.user
        user.password = make_password(password)
        user.save()
        user_token.delete()
        
        return redirect('userauths:password-reset-success')  # Redirect to a page indicating that the password has been reset
    
    return redirect('home')  # Redirect to home page if the request method is not POST

@password_reset_cooldown_required
def password_reset_cooldown(request):
    return render(request, 'password/password_reset_cooldown.html')


def redirect_sign_in(request):
    if request.user.is_authenticated:

        # Get the 'next' parameter from the URL, defaulting to None
        next_page = request.GET.get('next', None)

        if next_page:
            # If the 'next' parameter exists, redirect to that page
            return redirect(next_page)
        else:
            return redirect('core:index')

    return render(request, "userauths/sign-in.html")