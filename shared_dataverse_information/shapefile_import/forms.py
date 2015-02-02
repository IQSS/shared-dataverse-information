from django import forms

from .models import ShapefileImportData

from shared_dataverse_information.worldmap_api_helper.forms_api_validate import APIValidateHelperForm




class ShapefileImportDataForm(APIValidateHelperForm):

    def get_validation_field_names(self):
        return ('dv_user_email', 'shapefile_name')

    class Meta:
        model = ShapefileImportData

'''
# Original
class ShapefileImportDataForm(forms.ModelForm):
    """
    Used by WorldMap to validate incoming data from GeoConnect
    """

    class Meta:
        model = ShapefileImportData
'''
