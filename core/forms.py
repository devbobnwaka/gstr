
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate

from .models import User, FileUploader

class UserAuthenticationForm(forms.ModelForm):
    """
      Form for Logging in  users
    """
    password  = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model  =  User
        fields =  ('email', 'password')


    def __init__(self, *args, **kwargs):
        """
          specifying styles to fields 
        """
        super(UserAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'placeholder':'Password'})
        self.fields['email'].widget.attrs.update({'placeholder':'Email'})
        for field in (self.fields['email'],self.fields['password']):
            field.widget.attrs.update({'class': 'mb-10'})
            field.label=''

    def clean(self):
        if self.is_valid():

            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')



class UserCreationForm(UserCreationForm):
    password1  = forms.CharField(widget=forms.PasswordInput())
    password2  = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ("email","password1","password2")
        # fields = ("email",)

    def __init__(self, *args, **kwargs):
        """
          specifying styles to fields 
        """
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password2'].widget.attrs.update({'placeholder':'Password confirmation'})
        self.fields['password1'].widget.attrs.update({'placeholder':'Password'})
        self.fields['email'].widget.attrs.update({'placeholder':'Email'})
        for field in (self.fields['email'],self.fields['password1'],self.fields['password2']):
            field.widget.attrs.update({'class': 'mb-10'})
            field.label=''


class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)


class UploadFileForm(forms.ModelForm):
    # title = forms.CharField(max_length=50)
    # file = forms.FileField()
    class Meta:
        model = FileUploader
        fields = ('file_1', 'file_2',)
        widgets = {
            'file_1': forms.widgets.FileInput(attrs={'accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel'}),
            'file_2': forms.widgets.FileInput(attrs={'accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel'})
        }