from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Doctor, Appointment
from .forms import BookingForm
import razorpay
from django.views.decorators.csrf import csrf_exempt

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'appointments/doctor_list.html', {'doctors': doctors})

def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            date = form.cleaned_data['date']

            # create appointment (not paid yet)
            appt = Appointment.objects.create(
                doctor=doctor,
                patient_name=name,
                appointment_date=date
            )

            # create razorpay order
            amount = int(doctor.fee * 100)  # amount in paise
            order = razorpay_client.order.create(dict(amount=amount, currency='INR', payment_capture=1))
            appt.razorpay_order_id = order.get('id')
            appt.save()

            context = {
                'doctor': doctor,
                'appointment': appt,
                'order_id': order.get('id'),
                'amount': amount,
                'razorpay_key': settings.RAZORPAY_KEY_ID
            }
            return render(request, 'appointments/payment.html', context)
    else:
        form = BookingForm()
    return render(request, 'appointments/book_appointment.html', {'doctor': doctor, 'form': form})

@csrf_exempt
def payment_success(request):
    # Razorpay sends POST data back to success endpoint
    if request.method == "POST":
        data = request.POST
        payment_id = data.get('razorpay_payment_id')
        order_id = data.get('razorpay_order_id')
        signature = data.get('razorpay_signature')

        # verify the signature
        try:
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            razorpay_client.utility.verify_payment_signature(params_dict)
            appt = Appointment.objects.filter(razorpay_order_id=order_id).first()
            if appt:
                appt.is_paid = True
                appt.save()
            return render(request, 'appointments/success.html', {'appointment': appt})
        except Exception as e:
            print('Razorpay signature verification failed:', e)
            return render(request, 'appointments/cancel.html', {'error': str(e)})
    return redirect('/')


def payment_cancel(request):
    return render(request, 'appointments/cancel.html')
