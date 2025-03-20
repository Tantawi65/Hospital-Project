# hospital/forms.py
from django import forms
from django.contrib.auth.models import User
from . import models
from .models import Nurse
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone

# Existing forms (unchanged)
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class DoctorUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class DoctorForm(forms.ModelForm):
    class Meta:
        model = models.Doctor
        fields = ['address', 'mobile', 'department', 'status', 'profile_pic']

class PatientUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class PatientForm(forms.ModelForm):
    assignedDoctorId = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True), empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model = models.Patient
        fields = ['address', 'mobile', 'status', 'symptoms', 'profile_pic']

class NurseUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class NurseForm(forms.ModelForm):
    class Meta:
        model = models.Nurse
        fields = ['mobile', 'assignedWard', 'profile_pic']

class NurseLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

# Updated Appointment Forms
class AppointmentForm(forms.ModelForm):
    doctorId = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True), empty_label="Doctor Name and Department", to_field_name="user_id")
    patientId = forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True), empty_label="Patient Name and Symptoms", to_field_name="user_id")
    appointmentDate = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        label="Appointment Date and Time"
    )

    class Meta:
        model = models.Appointment
        fields = ['description', 'status', 'appointmentDate']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PatientAppointmentForm(forms.ModelForm):
    doctorId = forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True), empty_label="Doctor Name and Department", to_field_name="user_id")
    appointmentDate = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        label="Appointment Date and Time"
    )

    class Meta:
        model = models.Appointment
        fields = ['description', 'appointmentDate']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# New form for rescheduling appointments
class PatientRescheduleAppointmentForm(forms.ModelForm):
    appointmentDate = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        label="Appointment Date and Time"
    )

    class Meta:
        model = models.Appointment
        fields = ['description', 'appointmentDate']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Format the initial appointmentDate for datetime-local input
        if self.instance and self.instance.appointmentDate:
            self.initial['appointmentDate'] = self.instance.appointmentDate.strftime('%Y-%m-%dT%H:%M')

    def clean_appointmentDate(self):
        appointment_date = self.cleaned_data.get('appointmentDate')
        if appointment_date:
            # Ensure the date is in the future
            if appointment_date < timezone.now():
                raise forms.ValidationError("Appointment date must be in the future.")
            # Ensure the datetime is timezone-aware
            if not timezone.is_aware(appointment_date):
                appointment_date = timezone.make_aware(appointment_date)
        return appointment_date

class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))