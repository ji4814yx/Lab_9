from django import forms
from .models import Place


# Let's create a new class
class NewPlaceForm(forms.ModelForm):  # form of the web page related to the model
    class Meta:
        model = Place
        fields = ('name', 'visited')
