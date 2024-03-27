from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User, Contact



class UserRegisterForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Full Name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    phone_number = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    def clean_password2(self):
        # Since we're not using password2 field, return the password as confirmed password.
        return self.cleaned_data.get("password")
    

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['email', 'first_name','last_name','message', 'contact']
        widgets = {
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.EmailInput(),
            'contact': forms.TextInput(),
            'message': forms.Textarea(),
        }