from datetime import datetime

from django import forms

from .models import DataverseInfo

DATETIME_PAT_STR = '%Y-%m-%d %H:%M:%S'


class CheckForExistingLayerForm(forms.ModelForm):
#class EmbedLayerForm(forms.ModelForm):
    """Used to validate incoming data from GeoConnect

    Used for the API that retrieves a WorldMap Layer based on a specific:
        - Dataverse file id
        - Dataverse installation name
    """
    class Meta:
        model = DataverseInfo
        fields = ( 'datafile_id', 'dataverse_installation_name')
        #fields = ('dv_user_id', 'datafile_id')
