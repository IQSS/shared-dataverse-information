from django import forms

from .models import ShapefileImportData
from shared_dataverse_information.shared_form_util.version_help import can_use_fields_all


class ShapefileImportDataForm(forms.ModelForm):

    #def get_validation_field_names(self):
    #    return ('dv_user_email', 'shapefile_name')

    class Meta:
        model = ShapefileImportData
        if can_use_fields_all():
            fields = '__all__'

'''
# Original
class ShapefileImportDataForm(forms.ModelForm):
    """
    Used by WorldMap to validate incoming data from GeoConnect
    """

    class Meta:
        model = ShapefileImportData
'''
