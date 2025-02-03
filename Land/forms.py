#from django import forms
#from .models import Land

#class LandForm(forms.ModelForm):
 #   class Meta:
  #      model = Land
   #     fields = [
    #        'owner', 'title', 'description', 'location', 'size', 
     #       'length', 'width', 'land_type', 'price', 'image', 'listed_by'
      #  ]
       # widgets = {
        #    'description': forms.Textarea(attrs={'rows': 4}),
         ##   'size': forms.TextInput(attrs={'placeholder': 'Size must be in cm²'}),
           # 'length': forms.TextInput(attrs={'placeholder': 'Length must be in meters'}),
            #'width': forms.TextInput(attrs={'placeholder': 'Width must be in meters'}),
        #}
from django import forms
from .models import Land
# from django.contrib.auth.forms import UserCreationForm
from .models import User
# from .models import CustomUser


# class RegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2', 'user_type', 'phone']

class LandForm(forms.ModelForm):
    class Meta:
        model = Land
        # fields = ['owner', 'title', 'description', 'location', 'size', 'length', 'width', 'land_type', 'price', 'image', 'listed_by']

        fields = ['title', 'description', 'location', 'size', 'length', 'width', 'land_type', 'price', 'image']

