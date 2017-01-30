from django import forms

import time
from .models import ClassifyRequestData
from shared_dataverse_information.layer_classification.classify_format_helper import format_layer_name_for_classification


class ClassifyRequestDataForm(forms.ModelForm):

    def clean_layer_name(self):
        layer_name = self.cleaned_data.get('layer_name', None)
        if layer_name is None:
            raise forms.ValidationError(_('The layer name must be specified'), code='invalid')

        return format_layer_name_for_classification(layer_name)

    class Meta:
        model = ClassifyRequestData
        fields = '__all__'

class LayerAttributeRequestForm(forms.ModelForm):

    def clean_layer_name(self):
        layer_name = self.cleaned_data.get('layer_name', None)
        if layer_name is None:
            raise forms.ValidationError(_('The layer name must be specified'), code='invalid')

        return format_layer_name_for_classification(layer_name)

    class Meta:
        model = ClassifyRequestData
        fields =  ('layer_name', 'datafile_id', 'dataverse_installation_name' )
