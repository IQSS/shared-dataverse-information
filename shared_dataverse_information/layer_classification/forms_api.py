from django import forms

from .models import ClassifyRequestData

from shared_dataverse_information.worldmap_api_helper.forms_api_validate import APIValidateHelperForm


class ClassifyRequestDataForm(APIValidateHelperForm):

    def get_validation_field_names(self):
        return ('layer_name', 'attribute', 'method')

    class Meta:
        model = ClassifyRequestData

