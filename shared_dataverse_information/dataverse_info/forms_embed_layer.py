from datetime import datetime

from django import forms

from .models import DataverseInfo

from .forms_api_validate import APIValidateHelperForm

DATETIME_PAT_STR = '%Y-%m-%d %H:%M:%S'


class EmbedLayerForm(APIValidateHelperForm):
#class EmbedLayerForm(forms.ModelForm):
    """Used to validate incoming data from GeoConnect

    Used for the API that retrieves a WorldMap Layer based on a specific:
        - Dataverse file id

        xxx- Dataverse user id

    """
    layer = forms.CharField(label='layer name')
                
    def get_validation_field_names(self):
        return ( 'datafile_id',)
        #return ( 'dv_user_id',  'datafile_id',)

    def clean_layer(self):
        if hasattr(self, 'cleaned_data') is False:
            raise ValueError('Form is invalid.  cleaned_data is not available')

        layer = self.cleaned_data.get('layer')
        
        try:
            return layer.split(':')[-1]
        except:
            raise forms.ValidationError('The layer name is required')

            
    class Meta:
        model = DataverseInfo
        fields = ( 'datafile_id',)
        #fields = ('dv_user_id', 'datafile_id')

    
