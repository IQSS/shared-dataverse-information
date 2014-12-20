
from django.core.exceptions import ValidationError
from django import forms

from .models import MapLayerMetadata, KEY_MAPPING_FOR_DATAVERSE_API, DATAVERSE_REQUIRED_KEYS



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

    def format_data_for_dataverse_api(self, session_token_value=None):
        """
        Format the key names to make them compatible with the dataverse API

        :param session_token_value: if not specified, use the form's dv_session_token value
        :return: dict with formatted parameters
        """
        global KEY_MAPPING_FOR_DATAVERSE_API, DATAVERSE_REQUIRED_KEYS

        assert self.cleaned_data is not None, "cleaned_data not found.  Call and verify that form is_valid()"
        
        # If the session_token_value is not specified, 
        #   check for one in cleaned_data
        #
        # For the model/form, the session_token_value is optional
        #   
        if session_token_value is None:
            session_token_value = self.cleaned_data.get('dv_session_token')
                        
        assert session_token_value is not None, "A session token is required"
        assert session_token_value is not '', "A session token is required"
        print('dataversekeys: %s' % set(DATAVERSE_REQUIRED_KEYS))
        print('form keys: %s' %self.cleaned_data.keys())

        missing_required_keys = list(set(KEY_MAPPING_FOR_DATAVERSE_API.keys()) - set(self.cleaned_data.keys()))

        assert len(missing_required_keys) == 0, "Not all required keys found in form.  Required keys not found: %s" % missing_required_keys

        formatted_dict = {}
        for k, v in self.cleaned_data.items():
            worldmap_key = KEY_MAPPING_FOR_DATAVERSE_API.get(k, None)

            # make sure all the keys are there!
            assert worldmap_key is not None, "Key in MapLayerMetadata model not found in KEY_MAPPING_FOR_DATAVERSE_API api: %s" % k

            formatted_dict[worldmap_key] = v

        return formatted_dict





