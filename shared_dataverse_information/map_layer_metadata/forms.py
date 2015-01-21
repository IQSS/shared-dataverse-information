import re

from django import forms

from .models import MapLayerMetadata, WORLDMAP_SERVER_URL_BASE, KEY_MAPPING_FOR_DATAVERSE_API


class MapLayerMetadataValidationForm(forms.ModelForm):

    class Meta:
        model = MapLayerMetadata
        widgets = {  'dataverse_description': forms.Textarea(attrs={'rows': 2, 'cols':70})\
                    , 'dataset_description': forms.Textarea(attrs={'rows': 2, 'cols':70})\
               # , 'name': forms.TextInput(attrs={'size':20})
                }


class GeoconnectToDataverseDeleteMapLayerMetadataForm(forms.ModelForm):
    """
    Format values to delete map layer metadata from the Dataverse API
    
    This form ony has the field "dv_session_token"
    This form produces a dict with { token key name : token value }
    """
    class Meta:
        model = MapLayerMetadata
        fields = ('dv_session_token', )

    def format_for_dataverse_api(self):
        """
        Format the key names to make them compatible with the dataverse API

        :return: dict with formatted parameters
        """    
        global KEY_MAPPING_FOR_DATAVERSE_API

        assert self.cleaned_data is not None, "cleaned_data not found.  Call and verify that form is_valid()"
        
        return { KEY_MAPPING_FOR_DATAVERSE_API['dv_session_token'] : self.cleaned_data['dv_session_token'] }
        

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

    """
    Used to validate/format
    """
    def make_https_link_for_dev_prod(self, lnk):
        """
        Ensure dev and prod links are https -- they will be iframed on an https server
        """
        assert lnk is not None, "lnk cannot be None"

        lnk_lower = lnk.lower()
        
        # Don't force https for local host
        if lnk_lower.find('localhost') > -1 or lnk_lower.find('127.0.0.1') > -1 : 
            return lnk
            
        # Is this the worldmap server url?
        if lnk_lower.find(WORLDMAP_SERVER_URL_BASE) > -1:
            # Is https in use?
            if lnk_lower.find('https') == -1:     # No!        
                # No https, so make it https
                pattern = re.compile("http", re.IGNORECASE)
                lnk = pattern.sub("https", lnk)

        return lnk

    def clean_embed_map_link(self):
        """
        Make this https, if necessary
        """
        lnk = self.cleaned_data.get('embed_map_link', None)
        if lnk is None:
            raise forms.ValidationError(_('The embed_map_link must be specified'), code='invalid')

        return self.make_https_link_for_dev_prod(lnk)


    """
    def clean_map_image_link(self):
        lnk = self.cleaned_data.get('map_image_link', None)
        if lnk is None:
            raise forms.ValidationError(_('The map_image_link must be specified'), code='invalid')

        return self.make_https_link_for_dev_prod(lnk)
    """

