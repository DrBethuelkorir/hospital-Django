from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from patient.models import Patient
from patient.models import Payment

from patient.serializers import PatientSerializer
from patient.forms import PatientForm

from django.http import HttpResponse

from django_daraja.mpesa.core import MpesaClient

def index(request):
    if request.method == 'POST':
       form = UserCreationForm(request.POST)
       if form.is_valid():
           user = form.save()
           login(request, user)
           return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'index.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {
               'message' : 'Invalid username or password.'
            })

    return render(request, 'login.html')

def dashboard(request):
    patients = Patient.objects.all().order_by('-id')
    form = PatientForm()  
    
    return render(request, 'dashboard.html', {
        'patients': patients,
        'form': form,
        'p': patients[0] if patients else None
    })

def book_appointment(request):
    return render(request, 'bookappointment.html')

def profile(request):
    return render(request, 'profile.html')

def logout_user(request):
    logout(request)
    return redirect('login')

@require_POST
def add_patient(request):
    form = PatientForm(request.POST)
    if form.is_valid():
        p = form.save()
        return JsonResponse({
            'success': True,
            'patient': {
                'id':           p.pk,         
                'patient_id':   p.patient_id,
                'name':         p.name,
                'age':          p.age,
                'gender':       p.gender,
                'address':      p.address,
                'phone_number': p.phone_number,
                'email':        p.email,
            }
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)

@require_POST
def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.delete()
    
    return HttpResponse(status=204)

@require_POST
def update_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    form = PatientForm(request.POST, instance=patient)
    
    if form.is_valid():
        p = form.save()
        return JsonResponse({
            'success': True,
            'patient': {
                'id':           p.pk,         
                'patient_id':   p.patient_id,
                'name':         p.name,
                'age':          p.age,
                'gender':       p.gender,
                'address':      p.address,
                'phone_number': p.phone_number,
                'email':        p.email,
            }
        })
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)

from decimal import Decimal, ROUND_UP
from django.contrib import messages
from django.shortcuts import render, redirect

def make_payment(request):
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        phone_number = request.POST.get('phone_number')
        amount_str = request.POST.get('amount')

        # Keep the precise decimal for the DB record
        amount_decimal = Decimal(amount_str)

        # M-Pesa requires an integer; round up so you don't undercharge
        amount_int = int(amount_decimal.quantize(Decimal('1'), rounding=ROUND_UP))

        payment = Payment.objects.create(
            patient_name=patient_name,
            phone_number=phone_number,
            amount=amount_decimal,   # store the real amount
        )

        cl = MpesaClient()
        account_refrence = "HospitalPayment"
        transaction_desc = "Payment for hospital services"
        callback_url = "https://your-ngrok-url.ngrok-free.app/mpesa/callback/"

        response = cl.stk_push(
            phone_number,
            amount_int,         
            account_refrence,
            transaction_desc,
            callback_url,
        )

        payment.transaction_id = response.checkout_request_id
        payment.save()

        messages.success(request, 'Payment initiated successfully. Please complete the payment on your phone.')
        return redirect('dashboard')

    return render(request, 'make_payment.html')

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [AllowAny]