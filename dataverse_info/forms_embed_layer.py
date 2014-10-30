from datetime import datetime

from django.core.exceptions import ValidationError
from django import forms

from dataverse_info.models import DataverseInfo

from dataverse_info.forms_api_validate import APIValidateHelperForm

DATETIME_PAT_STR = '%Y-%m-%d %H:%M:%S'


class EmbedLayerForm(APIValidateHelperForm):
    """Used to validate incoming data from GeoConnect

    Used for the API that retrieves a WorldMap Layer based on a specific:
        - Dataverse user id
        - Dataverse file id
    """
    def get_validation_field_names(self):
        return ( 'dv_user_id',  'datafile_id')

    class Meta:
        model = DataverseInfo
        fields = ('dv_user_id', 'datafile_id')

    
