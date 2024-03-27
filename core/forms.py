from django import forms
from core.models import ProductReview, ClientChat
from userauths.models import User

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget=forms.Textarea(attrs={'placeholder': "Write review"}))

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']


class ClientChatForm(forms.ModelForm):
    class Meta:
        model = ClientChat
        fields = ['user', 'product', 'message']
        widgets = {
            'user': forms.HiddenInput(),
            'product': forms.HiddenInput(),
            'message': forms.Textarea(attrs={'placeholder': "Your message"}),
        }

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'phone_number']
        widgets = {
            'full_name': forms.TextInput(),
            'email': forms.EmailInput(),
            'phone_number': forms.TextInput(),
        }