from django import forms

from .models import ShapefileImportData


class ShapefileImportDataForm(forms.ModelForm):

    #def get_validation_field_names(self):
    #    return ('dv_user_email', 'shapefile_name')

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
