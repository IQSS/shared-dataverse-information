from datetime import datetime

from django import forms

from .models import DataverseInfo

#from shared_dataverse_information.worldmap_api_helper.forms_api_validate import APIValidateHelperForm

DATETIME_PAT_STR = '%Y-%m-%d %H:%M:%S'


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

