from datetime import datetime

from django import forms

from .models import DataverseInfo


DATETIME_PAT_STR = '%Y-%m-%d %H:%M:%S'


class DataverseInfoValidationForm(forms.ModelForm):
    """
    Used to validate incoming data from GeoConnect
    Excludes the map_layer attribute and create/modification times
    """

    def get_content_type(self):
        """
        Check the content_type attribute to see if it matches a known content_type
        """
        assert self.cleaned_data is not None, 'self.cleaned_data cannot be None.  Is this form valid? Have you called "is_valid()"'
        assert self.cleaned_data.has_key('content_type'), "cleaned_data does NOT have a 'content_type' key (this shouldn't be)"

        return self.cleaned_data['content_type']



    class Meta:
        model = DataverseInfo
        widgets = {  'dataverse_description': forms.Textarea(attrs={'rows': 2, 'cols':70})\
                    , 'dataset_description': forms.Textarea(attrs={'rows': 2, 'cols':70})\
               # , 'name': forms.TextInput(attrs={'size':20})
                }
        exclude = ['created', 'modified']
