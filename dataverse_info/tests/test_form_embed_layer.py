from __future__ import print_function
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from os.path import abspath, dirname, isfile, join

from django.test import TestCase
from django.http import HttpRequest

from dataverse_info.models import DataverseInfo
#from dataverse_info.forms import DataverseInfoValidationForm
from dataverse_info.forms_embed_layer import EmbedLayerForm
from dataverse_info.tests.msg_util import *

from django.conf import settings

import unittest
import json



class EmbedLayerFormTest(TestCase):
    
    def setUp(self):         
        settings.WORLDMAP_TOKEN_FOR_DATAVERSE = 'fake-token'
        self.test_data = dict(dv_user_id=321\
                    , datafile_id=960\
                    , layer='geonode:boston_commute'
                    )
        self.expected_clean_data = self.test_data
        
        self.expected_params = {'datafile_id': 960\
                    , 'dv_user_id': 321\
                    , 'SIGNATURE_KEY': '0f2246e1b7d0355f40b257dbe10d16afcdd2d6ece92d54d0d8843402'\
                    , 'layer' : 'geonode:boston_commute'
                    }
                    
        self.expected_params_bad_signature = {'datafile_id': 960\
                    , 'dv_user_id': 321\
                    , 'SIGNATURE_KEY': 'this-is-not-a-very-good-signature'\
                    , 'layer' : 'geonode:boston_commute'
                    }
        #f1 = EmbedLayerForm(self.test_data)
                    
    def test_workflow_01(self):
    
        msgt('(1) geoconnect, prepare initial data')
        f1 = EmbedLayerForm(self.test_data)

        msg('(a) Is data valid')
        self.assertEqual(f1.is_valid(), True)
        
        msg('(b) check validation field names')
        #msg(f.get_validation_field_names())
        self.assertEqual(f1.get_validation_field_names(), ('dv_user_id', 'datafile_id'))

        msg('(c) check signature generated with fake key')
        valid_signature = f1.get_api_signature()
        self.assertEqual(valid_signature, '0f2246e1b7d0355f40b257dbe10d16afcdd2d6ece92d54d0d8843402')

        msg('(d) check valid signature against data used to generate it')
        self.assertEqual(f1.is_signature_valid_check_val(valid_signature), True)
        
        msg('(e) cleaned data')
        self.assertEqual(f1.cleaned_data, self.expected_clean_data)

        msg('(f) cleaned data with signature key')
        self.assertEqual(f1.get_api_params_with_signature(), self.expected_params)
        
    #@unittest.skip("skipping")
    def test_workflow_02(self):
    
        msgt('(2) Generate params for API call')
        
        f1 = EmbedLayerForm(self.test_data)
        self.assertEqual(f1.is_valid(), True)
        

        msg('(a) Generate API call params')        
        self.assertEqual(f1.get_api_params_with_signature(), self.expected_params)

        msg('(b) Validate params in fresh form')
        f2 = EmbedLayerForm(self.expected_params)
        self.assertEqual(f2.is_valid(), True)
        
        msg('(c) Check signature validity.  Signature length too short')
        self.assertEqual(f2.is_signature_valid_check_val('signature - not long - enough')\
                        , False)

        msg('(d) Check signature validity.  Break assertion: signature is None')
        self.assertRaises(AssertionError, f2.is_signature_valid_check_val, None)
        
        msg('(e) Check signature validity.  Wrong signature')
        signature_str = '12345' * 11 
        self.assertEqual(f2.is_signature_valid_check_val(signature_str), False)
        
        msg('(f) Correct signature.')
        signature_str = '12345' * 11 
        self.assertEqual(f2.is_signature_valid_check_val(f1.get_api_signature()), True)

        msg('(g) cleaned data.')
        self.assertEqual(f2.cleaned_data, self.expected_clean_data)
        
    def test_workflow_03(self):
        msgt('(3) Try with HttpRequest')
        
        msg('(a) Try form with HttpRequest object')
        h = HttpRequest()
        h.POST = self.expected_params
        
        f1 = EmbedLayerForm(h.POST)
        self.assertEqual(f1.is_valid(), True)
        
        msg('(b) Try signature validity check - break assertion by sending dict, not HttpRequest')
        self.assertRaises(AssertionError, f1.is_signature_valid_check_request, h.POST)
            
            
        msg('(c) Try signature check with invalid data--no signature key')
        h_bad_data = HttpRequest()
        h_bad_data.POST = self.test_data 
        self.assertEqual(f1.is_signature_valid_check_request(h_bad_data), False)

        msg('(d) Try signature check with invalid data--bad signature key')
        h_bad_data2 = HttpRequest()
        h_bad_data2.POST = self.expected_params_bad_signature
        self.assertEqual(f1.is_signature_valid_check_request(h_bad_data2), False)

        msg('(e) Try signature check with valid data')
        self.assertEqual(f1.is_signature_valid_check_request(h), True)
        
        msg('(f) cleaned data.')
        self.assertEqual(f1.cleaned_data, self.expected_clean_data)
        
        
        
        
