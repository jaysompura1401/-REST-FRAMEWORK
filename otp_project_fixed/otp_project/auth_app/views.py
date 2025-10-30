
from django.shortcuts import render, redirect
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import random
from .models import UserOTP
from .forms import RegisterForm

def normalize_phone(phone, default_country_code='+91'):
    """
    Normalize phone number to E.164-like format.
    - If phone already starts with '+', return as-is.
    - If it starts with '00', replace with '+'.
    - If it starts with a single '0', remove it and add default country code.
    - Otherwise, prepend default country code.
    NOTE: This is a best-effort helper. For production, use a library like `phonenumbers`.
    """
    phone = phone.strip()
    if phone.startswith('+'):
        return phone
    if phone.startswith('00'):
        return '+' + phone[2:]
    if phone.startswith('0'):
        # remove leading 0 and prepend country code
        return default_country_code + phone[1:]
    # no plus and no leading zero -- assume local number, prepend country code
    return default_country_code + phone

def send_otp(phone, otp):
    """
    Send OTP using Twilio. This function raises TwilioRestException on failure.
    The caller should handle exceptions to avoid crashing the view.
    """
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP for registration is {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone
    )
    return message.sid

def register(request):
    msg = ""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone_raw = form.cleaned_data['phone']
            phone = normalize_phone(phone_raw)
            otp = str(random.randint(100000, 999999))

            # create or update user otp record
            user_obj, created = UserOTP.objects.update_or_create(
                phone=phone,
                defaults={'name': name, 'otp': otp, 'is_verified': False}
            )

            # Attempt to send OTP, but handle Twilio errors gracefully
            try:
                sid = send_otp(phone, otp)
                request.session['phone'] = phone
                msg = "OTP sent successfully. Check your phone."
                return redirect('verify_otp')
            except TwilioRestException as e:
                # Log error (print for development). Provide friendly message to user.
                print("Twilio error:", e)
                # Check for common error code 21608 (trial account / unverified number)
                err_msg = str(e)
                if '21608' in err_msg or 'unverified' in err_msg.lower():
                    msg = ("Twilio trial account cannot send to unverified numbers. "
                           "Either verify this recipient number in your Twilio console "
                           "or upgrade/purchase a Twilio number.")
                else:
                    msg = "Failed to send OTP due to an error with the SMS provider."
        else:
            msg = "Form is not valid. Please correct the errors."
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form, 'msg': msg})

def verify_otp(request):
    phone = request.session.get('phone')
    user = UserOTP.objects.filter(phone=phone).first()
    msg = ""

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if user and user.otp == entered_otp:
            user.is_verified = True
            user.save()
            msg = "OTP verified successfully!"
        else:
            msg = "Invalid OTP. Try again."

    return render(request, 'verify_otp.html', {'phone': phone, 'msg': msg})
