from django.core.exceptions import ValidationError
from django import forms

from shapefile_import.models import ShapefileImportData


class ShapefileImportDataForm(forms.ModelForm):
    """
    Used by WorldMap to validate incoming data from GeoConnect
    """

    class Meta:
        model = ShapefileImportData
