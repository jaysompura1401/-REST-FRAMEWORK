from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']

        # Here, you can save the user to the database if needed

        subject = "Registration Successful!"
        message = f"Hi {username},\n\nThank you for registering on our website. Your registration was successful!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        messages.success(request, "Registration successful! Confirmation email sent.")
        return redirect('register')

    return render(request, 'register.html')

from django.shortcuts import render

def register_user(request):
    return render(request, 'accounts/register.html')  # 👈 include app name here
