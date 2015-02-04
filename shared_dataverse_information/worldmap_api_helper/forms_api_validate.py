import hashlib
import time

from django.core.handlers import wsgi

from django import forms
from django.http import HttpRequest
from django.conf import settings

SIGNATURE_KEY = 'SIGNATURE_KEY'

class APIValidateHelperForm(forms.ModelForm):
    """
    Abstract form for API use.
    
    How to use:
        (a) Create a new form object which inherits from this one.
            Example:
            
            CheckForExistingLayerForm(APIValidateHelperForm)
            
        (b) On the new form object, make the following changes:
        
            (1) Overwrite the "def get_validate_field_names" method.

                Return a list of fields whose values will be used to create the signature key
                Example:

                def get_validation_field_names(self):
                    return ('datafile_id', 'dataverse_installation_name')
                
            (2) Define the model and fields to be used for the new form object
                Example:
                
                class Meta:
                    model = DataverseInfo
                    
        (c) Full example:

            class CheckForExistingLayerForm(APIValidateHelperForm):

                def get_validation_field_names(self):
                    return ('datafile_id', 'dataverse_installation_name')

                class Meta:
                    model = DataverseInfo
                
    When a POST request is received by GeoConnect or WorldMap, methods on this form are used for valiation.    

    PARAMS SENT TO API: { 'dv_user_id' : '--val--'
                        ,  'datafile_id' : '--val--'
                        ... (and all other DataverseInfo fields) ...
                        , 'SIGNATURE_KEY' : 'a4337bc45a8fc544c03f52dc550cd6e1e87021bc896588bd79e901e2'
                  }
                  
    Note: "SIGNATURE_KEY" param is handled outside of this form 
            and is sent separately to the "is_signature_valid(self, signature_value)" method
    
        
    """
    def get_validation_field_names(self):
        """
        Abstract.  Implement this for each form

        example:
        return ( 'dv_user_id',  'datafile_id')

        """
        raise AssertionError('This method must be implemented for each Form: %s' % type(self))


    def get_api_signature(self):
        """
        Used internally to generate the "SIGNATURE_KEY" parameter
        """
        assert hasattr(self, 'cleaned_data'), "Form is invalid.  cleaned_data is not available"
        
        val_list = []
        for key in self.get_validation_field_names():
            val = self.cleaned_data.get(key, None)
            if val is None:
                raise ValueError('Value for key "%s" cannot be None' % key)
            val_list.append('%s' % val)
            
        val_str = '|'.join(val_list + [settings.WORLDMAP_TOKEN_FOR_DATAVERSE])
        
        
        return hashlib.sha224(val_str).hexdigest()
    
    def get_timestamp_string(self):
        return str(time.time())
        
    def is_signature_valid_check_val(self, signature_value):
        """
        After the form is found to be valid
        """
        assert signature_value is not None, "signature_value cannot be None"
        
        if hasattr(self, 'cleaned_data') is False:
            raise ValueError('Form is invalid.  cleaned_data is not available')

        if len(signature_value) < 50:
            return False
        
        #print 'post sig: %s' % signature_value
        #print 'calculated sig: %s' % self.get_api_signature()
        
        if self.get_api_signature() == signature_value:
            return True
        return False
        
    
    def do_attributes_match(self, **attribute_dict):
        assert type(attribute_dict) is dict, "attribute_dict must be type dict"
        assert hasattr(self, 'cleaned_data'), "Form is invalid.  cleaned_data is not available"
        
        for key in self.get_validation_field_names():
            val = attribute_dict.get(key, None)
            if val is None or not val == self.cleaned_data.get(key, None):
                return False
        
        return True

        
    def get_api_params_with_signature(self):
        """
        Return a dictionary with all of the form data 
        AND a calculated SIGNATURE_KEY
        """
        assert hasattr(self, 'cleaned_data'), "Form is invalid.  cleaned_data is not available"
        
        params = self.cleaned_data
        params[SIGNATURE_KEY] = self.get_api_signature()
        return params
    
    
    def is_signature_valid_check_post(self, request_obj):    
        assert isinstance(request_obj, HttpRequest) or isinstance(request_obj, wsgi.WSGIRequest)\
                    ,'request_obj must be a HttpRequest or WSGIRequest object'

        if not request_obj.POST:
            return False
            
        if not request_obj.POST.has_key(SIGNATURE_KEY):
            return False
            
        key_val = request_obj.POST.get(SIGNATURE_KEY, None)
        if key_val is None or len(key_val)==0:
            return False
        
        #print '-' * 40
        #print 'request_obj.POST', request_obj.POST
        #print 'SIGNATURE_KEY from request: %s' % key_val
        #print '-' * 40
        
        return self.is_signature_valid_check_val(key_val)
   
   
   
    '''
    def is_signature_valid_check_get(self, request_obj):
        """
        Wouldn't actually use, need proper private/public keys
        """
        if not type(request_obj) in (HttpRequest, wsgi.WSGIRequest):
            raise AssertionError('request_obj must be a HttpRequest or WSGIRequest object')
            
        if not request_obj.GET:
            return False
            
        if not request_obj.GET.has_key(SIGNATURE_KEY):
            return False
            
        key_val = request_obj.GET.get(SIGNATURE_KEY, None)
        if key_val is None:
            return False
        
        return self.is_signature_valid_check_val(key_val)
    '''
    

        
    
    
    class Meta:
        abstract = True
