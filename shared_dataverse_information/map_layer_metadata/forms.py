
from django.core.exceptions import ValidationError
from django import forms

from map_layer_metadata.models import MapLayerMetadata, KEY_MAPPING_FOR_DATAVERSE_API, DATAVERSE_REQUIRED_KEYS



class MapLayerMetadataValidationForm(forms.ModelForm):
    """
    Used to validate/format
    """
    class Meta:
        model = MapLayerMetadata
        widgets = {  'dataverse_description': forms.Textarea(attrs={'rows': 2, 'cols':70})\
                    , 'dataset_description': forms.Textarea(attrs={'rows': 2, 'cols':70})\
               # , 'name': forms.TextInput(attrs={'size':20})
                }

    def format_data_for_dataverse_api(self, session_token_value):
        """
        Format the key names to make them compatible with the dataverse API

        :param session_token_value:
        :return:
        """
        global KEY_MAPPING_FOR_DATAVERSE_API, DATAVERSE_REQUIRED_KEYS

        assert self.cleaned_data is not None, "cleaned_data not found.  Call and verify that form is_valid()"
        assert session_token_value is not None, "A session token is required"

        missing_required_keys = list(set(DATAVERSE_REQUIRED_KEYS.keys()) - set(self.cleaned_data.keys()))

        assert len(missing_required_keys) == 0, "Not all required keys found in form.  Required keys not found: %s" % missing_required_keys

        formatted_dict = {}
        for k, v in self.cleaned_data.items():
            worldmap_key = KEY_MAPPING_FOR_DATAVERSE_API.get(k, None)

            # make sure all the keys are there!
            assert worldmap_key is not None, "Key in MapLayerMetadata model not found in KEY_MAPPING_FOR_DATAVERSE_API api: %s" % k

            formatted_dict['worldmap_key'] = v

        return formatted_dict





