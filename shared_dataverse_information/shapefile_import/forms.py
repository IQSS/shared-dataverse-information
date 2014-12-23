from django import forms

from .models import ShapefileImportData


class ShapefileImportDataForm(forms.ModelForm):
    """
    Used by WorldMap to validate incoming data from GeoConnect
    """

    class Meta:
        model = ShapefileImportData
