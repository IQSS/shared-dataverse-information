from django import forms

from .models import ClassifyRequestData

from shared_dataverse_information.worldmap_api_helper.forms_api_validate import APIValidateHelperForm


class ClassifyRequestDataForm(APIValidateHelperForm):

    def get_validation_field_names(self):
        return ('layer_name', 'attribute', 'method')

    def clean_layer_name(self):
        """
        "geonode:my_layer_name" becomes "my_layer_name"
        "my_layer_name" stays "my_layer_name"
        """
        layer_name = self.cleaned_data.get('layer_name', None)
        if layer_name is None:
            raise forms.ValidationError(_('The layer name must be specified'), code='invalid')

        return layer_name.split(':')[-1]
            
    class Meta:
        model = ClassifyRequestData

