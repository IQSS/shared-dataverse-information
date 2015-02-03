from datetime import datetime

from django import forms

from .models import DataverseInfo

from shared_dataverse_information.worldmap_api_helper.forms_api_validate import APIValidateHelperForm

DATETIME_PAT_STR = '%Y-%m-%d %H:%M:%S'


class CheckForExistingLayerForm(APIValidateHelperForm):
#class EmbedLayerForm(forms.ModelForm):
    """Used to validate incoming data from GeoConnect

    Used for the API that retrieves a WorldMap Layer based on a specific:
        - Dataverse file id
        - Dataverse installation name
    """
                
    def get_validation_field_names(self):
        return ('datafile_id', 'dataverse_installation_name')
        #return ( 'dv_user_id',  'datafile_id',)

            
    class Meta:
        model = DataverseInfo
        fields = ( 'datafile_id', 'dataverse_installation_name')
        #fields = ('dv_user_id', 'datafile_id')


class DataverseInfoValidationFormWithKey(APIValidateHelperForm):
    """
    Used for Delete requests
    """
    def get_validation_field_names(self):
        return ('datafile_id', 'dataverse_installation_name')

    class Meta:
        model = DataverseInfo
        exclude = ['created', 'modified']
            #exclude = ['map_layer','created', 'modified']
    
    
    
