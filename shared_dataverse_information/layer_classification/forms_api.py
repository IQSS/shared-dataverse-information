from django import forms

import time
from .models import ClassifyRequestData
from shared_dataverse_information.worldmap_api_helper.forms_api_validate import APIValidateHelperForm
from shared_dataverse_information.layer_classification.classify_format_helper import format_layer_name_for_classification


class ClassifyRequestDataForm(APIValidateHelperForm):

    def get_validation_field_names(self):
        return ('layer_name', 'attribute', 'method', 'datafile_id', 'dataverse_installation_name')
            
    def clean_layer_name(self):
        layer_name = self.cleaned_data.get('layer_name', None)
        if layer_name is None:
            raise forms.ValidationError(_('The layer name must be specified'), code='invalid')
        
        return format_layer_name_for_classification(layer_name)

            
    class Meta:
        model = ClassifyRequestData


class LayerAttributeRequestForm(APIValidateHelperForm):

    def get_validation_field_names(self):
        return ('layer_name', 'datafile_id', 'dataverse_installation_name')

    def clean_layer_name(self):
        layer_name = self.cleaned_data.get('layer_name', None)
        if layer_name is None:
            raise forms.ValidationError(_('The layer name must be specified'), code='invalid')

        return format_layer_name_for_classification(layer_name)

    class Meta:
        model = ClassifyRequestData
        fields =  ('layer_name', 'datafile_id', 'dataverse_installation_name' )