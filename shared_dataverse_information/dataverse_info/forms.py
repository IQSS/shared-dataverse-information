from datetime import datetime

from django.core.exceptions import ValidationError
from django import forms

from dataverse_info.models import DataverseInfo

from dataverse_info.forms_api_validate import APIValidateHelperForm

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
        #exclude = ['map_layer','created', 'modified']


class CheckForExistingLayerFormBasic(forms.ModelForm):
    """
    Used for the API that retrieves a WorldMap Layer based on a specific:
        - Dataverse user id
        - Dataverse file id
    """
    class Meta:
        model = DataverseInfo
        fields = ('dv_user_id', 'datafile_id')



class CheckForDataverseUserLayersFormBasic(forms.ModelForm):
    """
    Used for the API that retrieves a Dataverse user's WorldMap Layers
        - input dv_user_id
    """
    class Meta:
        model = DataverseInfo
        fields = ('dv_user_id',)
