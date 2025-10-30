# Stripe Doctor Appointment (Lab Example) - Free/Test Mode
Follow these steps to run the project locally (test mode - no charge):
1. Create virtualenv and activate it:
   python -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
2. Install requirements:
   pip install -r requirements.txt
3. Set Stripe test keys as environment variables OR edit stripe_doctor/settings.py:
   export STRIPE_PUBLISHABLE_KEY='pk_test_xxx'
   export STRIPE_SECRET_KEY='sk_test_xxx'
   export DJANGO_SECRET_KEY='some_secret'
   # On Windows PowerShell use: $env:STRIPE_PUBLISHABLE_KEY='pk_test_xxx' etc.
4. Migrate and create superuser:
   python manage.py migrate
   python manage.py createsuperuser
5. Run server:
   python manage.py runserver
6. Add Doctor entries via admin and test booking. Use Stripe test card 4242 4242 4242 4242.
