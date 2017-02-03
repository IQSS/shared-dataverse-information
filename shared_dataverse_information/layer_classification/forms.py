"""ClassifyLayerForm - Form used for styling a layer"""

from django.utils.translation import ugettext_lazy as _
from django import forms
from shared_dataverse_information.layer_classification.models\
    import ClassificationMethod, ColorRamp

from shared_dataverse_information.worldmap_api_helper.url_helper\
    import CLASSIFY_LAYER_API_PATH
from shared_dataverse_information.layer_classification.classify_format_helper\
    import format_layer_name_for_classification

INITIAL_SELECT_CHOICE = ('', 'Select...')

def get_classify_method_choices():
    """Get ClassificationMethod values for form dropdown"""

    queryset = ClassificationMethod.objects.filter(active=True)

    return [INITIAL_SELECT_CHOICE] +\
           [(x.id, x.display_name) for x in queryset]

def get_classify_string_choices():
    """Get string method ClassificationMethod values for form dropdown"""

    queryset = ClassificationMethod.objects.filter(\
                            active=True,
                            is_string_usable=True)

    return [INITIAL_SELECT_CHOICE] +\
           [(x.id, x.display_name) for x in queryset]

def get_color_ramp_choices():
    """Get ColorRamp values for form dropdown"""
    queryset = ColorRamp.objects.filter(active=True)

    return [INITIAL_SELECT_CHOICE] +\
            [(x.id, x.display_name) for x in queryset]

ATTRIBUTE_VALUE_DELIMITER = '|'
FIELD_CSS_ATTRS = {'class':'form-control input-sm'}


class ClassifyLayerForm(forms.Form):
    """
    Evaluate classification parameters to be used for a new layer style
    """
    layer_name = forms.CharField(widget=forms.HiddenInput())

    data_source_type = forms.CharField(widget=forms.HiddenInput())

    attribute = forms.ChoiceField(\
                    choices=[(-1, 'Error: no choices available')],
                    widget=forms.Select(attrs=FIELD_CSS_ATTRS))

    method = forms.ChoiceField(\
                    label='Classification Method',
                    choices=(),
                    widget=forms.Select(attrs=FIELD_CSS_ATTRS))

    intervals = forms.IntegerField(\
                        label='Intervals',
                        initial=5,
                        widget=forms.NumberInput(attrs=FIELD_CSS_ATTRS))

    ramp = forms.ChoiceField(label='Colors',
                             choices=(),
                             widget=forms.Select(attrs=FIELD_CSS_ATTRS))

    def __init__(self, *args, **kwargs):
        """Initialize with a layer name and attribute information
            (a) layer_name
                - Name of layer to classify.
                - Example: "geonode:social_disorder_shapefile_zip_fif"

            (b) data source type:
                - TYPE_SHAPEFILE_LAYER, TYPE_JOIN_LAYER, TYPE_LAT_LNG_LAYER, etc
                - values from geoconnect
            (b) raw_attribute_info
                - list containing attributes associated with dataset.
                - Each attribute is a dict.
                - Example: [{"type": "double",
                              "display_name": "Area",
                              "name": "AREA"},
                               ... (etc) ... ]
        """
        layer_name = kwargs.pop('layer_name', None)
        assert layer_name is not None, "layer_name is required in kwargs"

        data_source_type = kwargs.pop('data_source_type', None)
        assert data_source_type is not None, "data_source_type is required in kwargs"

        raw_attribute_info = kwargs.pop('raw_attribute_info', None)
        assert isinstance(raw_attribute_info, list) or isinstance(raw_attribute_info, tuple)\
                , "raw_attribute_info must be a list or tuple"

        # Initialize form
        super(ClassifyLayerForm, self).__init__(*args, **kwargs)

        self.fields['method'].choices = get_classify_method_choices()
        self.fields['ramp'].choices = get_color_ramp_choices()


        # Initialize the "layer_name" and "data_source_type" fields
        self.fields['layer_name'].initial = layer_name
        self.fields['data_source_type'].initial = data_source_type

        # Format attribute information
        attribute_choices = ClassifyLayerForm.format_attributes_for_form(raw_attribute_info)
        # Initialize "attribute" field with the formatted attribute information
        self.fields['attribute'] = forms.ChoiceField(\
                                choices=attribute_choices,
                                widget=forms.Select(attrs=FIELD_CSS_ATTRS))


    @staticmethod
    def format_attributes_for_form(attr_info):
        """
        example of item in 'raw list'
            {"display_name": "Objectid", "type": "long", "name": "OBJECTID"},

        formatted item:
            ('long|OBJECTID', 'Objectid')
        """
        if attr_info is None or len(attr_info) == 0:
            return [('-1', 'Information not found')]

        choice_tuples = [INITIAL_SELECT_CHOICE]

        for attr in attr_info:
            # (1) Make sure everything is a dict
            #   and all attributes exist
            #
            if not type(attr) is dict:
                continue        # skip non dicts
            if not (attr.has_key('type') and\
                attr.has_key('name') and\
                attr.has_key('display_name')):
                continue    # skip missing keys

            # (2) Remove "unnamed" attribute
            #
            if attr['name'] == '_unnamed' and attr['display_name'] == '_unnamed':
                continue

            choice_val = '%s%s%s' % (\
                                    attr['type'],
                                    ATTRIBUTE_VALUE_DELIMITER,
                                    attr['name'])
            choice_pair = (choice_val, attr['display_name'])
            choice_tuples.append(choice_pair)      # add choice

        if len(choice_tuples) == 0:
            return [('-1', 'Information not found')]

        return choice_tuples


    @staticmethod
    def get_classify_choices():
        """Get all ClassificationMethod objects"""
        return ClassificationMethod.objects.filter(active=True)


    @staticmethod
    def get_classify_non_string_choices():
        """Get non-string ClassificationMethod objects"""
        return ClassificationMethod.objects.filter(active=True, is_string_usable=False)


    @staticmethod
    def get_classify_string_choices():
        """Get string-only ClassificationMethod objects"""
        return ClassificationMethod.objects.filter(active=True, is_string_usable=True)


    def clean_ramp(self):
        """clean the 'ramp'"""
        color_ramp_id = self.cleaned_data.get('ramp', None)
        if color_ramp_id is None:
            raise forms.ValidationError(_('Color ramp must be specified'), code='invalid')

        try:
            color_ramp_obj = ColorRamp.objects.filter(active=True).get(pk=color_ramp_id)
        except ColorRamp.DoesNotExist:
            raise forms.ValidationError(\
                    _('This value is not an active ColorRamp id: %(value)s'),
                    params={'value': color_ramp_id})
            #raise Exception('This value is not an active ColorRamp id')

        return color_ramp_obj

    def clean_method(self):
        """clean the 'method'"""
        method_id = self.cleaned_data.get('method', None)
        if method_id is None:
            raise forms.ValidationError(\
                    _('The classification method must be specified'),
                    code='invalid')

        try:
            method_obj = ClassificationMethod.objects.filter(active=True).get(pk=method_id)
        except ClassificationMethod.DoesNotExist:
            raise forms.ValidationError(\
                    _('This value is not an active classification id: %(value)s'),\
                    params={'value': method_id})

        return method_obj

    def get_worldmap_classify_api_url(self):
        """Get classify url for API call"""
        if not self.is_valid:
            return None

        layer_name = self.cleaned_data.get('layer_name', None)
        if layer_name is None:
            return None

        return CLASSIFY_LAYER_API_PATH


    def clean_attribute(self):
        """clean the 'attribute'"""
        attribute = self.cleaned_data.get('attribute', None)
        if attribute is None:
            raise forms.ValidationError(_('The attribute must be specified'), code='invalid')

        return attribute.split(ATTRIBUTE_VALUE_DELIMITER)[-1]

    def clean_intervals(self):
        """clean the 'intervals'"""
        num_bins = self.cleaned_data.get('intervals', None)
        if num_bins is None:
            raise forms.ValidationError(\
                    _('The number of intervals must be specified'),
                    code='invalid')

        print 'num_bins', type(num_bins)
        if num_bins < 1:
            raise forms.ValidationError(\
                    _('The number of intervals must be 1 or greater'),
                    code='invalid')

        if num_bins > 300:
            raise forms.ValidationError(
                _('The number of intervals must be less than that!'),
                code='invalid')

        return num_bins


    def clean_layer_name(self):
        """
        "geonode:my_layer_name" becomes "my_layer_name"
        "my_layer_name" stays "my_layer_name"
        """
        layer_name = self.cleaned_data.get('layer_name', None)
        if layer_name is None:
            raise forms.ValidationError(_('The layer name must be specified'), code='invalid')

        return format_layer_name_for_classification(layer_name)


    def get_params_for_display(self):
        """Get parameters for display"""
        if not self.is_valid():
            return None

        form_vals = self.cleaned_data.copy()


        color_ramp_obj = form_vals['ramp']

        params = {\
                    'layer_name' : form_vals['layer_name'],
                    'attribute' : form_vals['attribute'],
                    'intervals' : form_vals['intervals'],
                    'method' :  form_vals['method'].display_name,
                    'ramp' :  color_ramp_obj.display_name,
                    'startColor' :  color_ramp_obj.start_color,
                    'endColor' :  color_ramp_obj.end_color,
                    'reverse' : False}
        return params

    def get_params_dict_for_classification(self):
        """Get parameters for classification"""

        if not self.is_valid():
            return None

        form_vals = self.cleaned_data.copy()

        color_ramp_obj = form_vals['ramp']

        params = {\
                    'layer_name' : form_vals['layer_name'],
                    'attribute' : form_vals['attribute'],
                    'intervals' : form_vals['intervals'],
                    'method' :  form_vals['method'].value_name,
                    'ramp' :  color_ramp_obj.value_name,
                    'startColor' :  color_ramp_obj.start_color,
                    'endColor' :  color_ramp_obj.end_color,
                    'reverse' : False}
        return params


'''
if __name__=='__main__':
    f = ClassifyLayerForm(initial={'layer_name': 'income_abadfe'}\
                            , attribute_choices=[ (1, 'one'), (2, 'two')]\
                        )
    print f
'''
