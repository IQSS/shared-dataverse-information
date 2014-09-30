from django.core.exceptions import ValidationError

from django import forms
from dataverse_info.models import DataverseInfo

# Create the form class.
class DataverseInfoValidationForm(forms.ModelForm):
    """Used to validate incoming data from GeoConnect
    Excludes the map_layer attribute and create/modtimes
    """
    
    class Meta:
        model = DataverseInfo
        widgets = {  'dataverse_description': forms.Textarea(attrs={'rows': 2, 'cols':70})\
                    , 'dataset_description': forms.Textarea(attrs={'rows': 2, 'cols':70})\
               # , 'name': forms.TextInput(attrs={'size':20}) 
                }
        exclude = ['created', 'modified']
        #exclude = ['map_layer','created', 'modified']

