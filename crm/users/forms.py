# users/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class UserRegistrationForm(forms.ModelForm):
    """
    Form for registering a new Connector or Staff user.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone', 'name', 'role')
        # Ensure only non-Admin roles can be registered via this form
        widgets = {
            'role': forms.Select(choices=[
                ('STAFF', 'Staff'),
                ('CONNECTOR', 'Connector')
            ]),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class PhoneAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form that uses 'phone' instead of 'username'.
    """
    username = forms.CharField(label='Phone Number', max_length=15)
    
    # We must explicitly rename 'username' to 'phone' when accessing data
    def clean(self):
        # We need to use the parent's clean method to handle authentication logic
        # by temporarily renaming the field back to 'username' for compatibility.
        self.data = self.data.copy()
        self.data['username'] = self.data.pop('phone', None)
        
        # Call the parent's clean method
        cleaned_data = super().clean()
        
        # Rename back for context if needed, though the super().clean() usually handles the auth check.
        if 'username' in cleaned_data:
            cleaned_data['phone'] = cleaned_data.pop('username')
            
        return cleaned_data