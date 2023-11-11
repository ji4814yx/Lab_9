from django import forms
from django.forms import FileInput, DateInput
from .models import Place


# Let's create a new class
class NewPlaceForm(forms.ModelForm):  # form of the web page related to the model
    class Meta:
        model = Place
        fields = ('name', 'visited')


class TripReviewForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('notes', 'date_visited', 'photo') # the form has 3 fields: note, date_visited, and photo
        widgets = {
            'date_visited': DateInput()
        }
