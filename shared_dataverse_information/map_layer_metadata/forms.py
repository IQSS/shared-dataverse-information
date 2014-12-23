
from django import forms

from .models import MapLayerMetadata, KEY_MAPPING_FOR_DATAVERSE_API


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

class GeoconnectToDataverseMapLayerMetadataValidationForm(forms.ModelForm):

    class Meta:
        model = MapLayerMetadata
        exclude = ('download_links', 'attribute_info')

    def format_data_for_dataverse_api(self, session_token_value=None):
        """
        Format the key names to make them compatible with the dataverse API

        :param session_token_value: if not specified, use the form's dv_session_token value
        :return: dict with formatted parameters
        """
        global KEY_MAPPING_FOR_DATAVERSE_API

        assert self.cleaned_data is not None, "cleaned_data not found.  Call and verify that form is_valid()"
        
        # If the session_token_value is specified, use that one
        #   Note: For form validation, the session_token_value is optional
        #   
        if session_token_value is not None:
            self.cleaned_data['dv_session_token'] = session_token_value
        
        # A session token IS required for this formatting
        if not self.cleaned_data.get('dv_session_token'):
            raise ValueError("A session token is required for updating Dataverse Metadata")        

        formatted_dict = {}
        for k, v in self.cleaned_data.items():
            worldmap_key = KEY_MAPPING_FOR_DATAVERSE_API.get(k, None)

            # make sure all the keys are there!
            assert worldmap_key is not None, "Key in MapLayerMetadata model not found in KEY_MAPPING_FOR_DATAVERSE_API api: %s" % k

            formatted_dict[worldmap_key] = v

        return formatted_dict

#missing_required_keys = list(set(KEY_MAPPING_FOR_DATAVERSE_API.keys()) - set(self.cleaned_data.keys()))
#assert len(missing_required_keys) == 0, "Not all required keys found in form.  Required keys not found: %s" % missing_required_keys


class WorldMapToGeoconnectMapLayerMetadataValidationForm(forms.ModelForm):
    """
    Used to validate/format
    """
    class Meta:
        model = MapLayerMetadata
        exclude = ('dv_session_token',)


