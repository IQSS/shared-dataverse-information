from __future__ import print_function
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from os.path import abspath, dirname, isfile, join

from django.test import TestCase
from django.http import HttpRequest

from shared_dataverse_information.dataverse_info.models import DataverseInfo
#from dataverse_info.forms import DataverseInfoValidationForm
from shared_dataverse_information.dataverse_info.forms_existing_layer import CheckForExistingLayerForm
from shared_dataverse_information.dataverse_info.tests.msg_util import *

from django.conf import settings

import unittest
import json



class EmbedLayerFormTest(TestCase):
    
    def setUp(self):         
        settings.WORLDMAP_TOKEN_FOR_DATAVERSE = 'fake-token'
        self.test_data = dict(datafile_id=960\
                    , dataverse_installation_name='HU dataverse!'\
                    #, layer='geonode:boston_commute'
                    )
        self.expected_clean_data = self.test_data
        
        self.expected_params = {'datafile_id': 960\
                    , 'dataverse_installation_name': u'HU dataverse!'\
                    , 'SIGNATURE_KEY': '0068e42806f42ed64ca1ba3e9f3f1549c9bef3fcd84dacaf79ea18e7'\
                    #, 'layer' : 'geonode:boston_commute'
                    }
                    
        self.expected_params_bad_signature = {'datafile_id': 960\
                    , 'dataverse_installation_name': u'HU dataverse!'\
                    , 'SIGNATURE_KEY': 'this-is-not-a-very-good-signature'\
                    #, 'layer' : 'geonode:boston_commute'
                    }
        #f1 = EmbedLayerForm(self.test_data)
                    
    def test_workflow_01(self):
    
        msgt('(1) geoconnect, prepare initial data')
        f1 = CheckForExistingLayerForm(self.test_data)

        msg('(a) Is data valid')
        self.assertEqual(f1.is_valid(), True)

        msg('(b) check validation field names')
        #msg(f.get_validation_field_names())
        self.assertEqual(f1.get_validation_field_names(), ('datafile_id', 'dataverse_installation_name'))

        msg('(c) check signature generated with fake key')
        valid_signature = f1.get_api_signature()
        self.assertEqual(valid_signature, '0068e42806f42ed64ca1ba3e9f3f1549c9bef3fcd84dacaf79ea18e7')


        msg('(d) check valid signature against data used to generate it')
        self.assertEqual(f1.is_signature_valid_check_val(valid_signature), True)

        msg('(e) cleaned data')
        self.assertEqual(f1.cleaned_data, self.expected_clean_data)

        msg('(f) cleaned data with signature key')
        self.assertEqual(f1.get_api_params_with_signature(), self.expected_params)
        
    def test_workflow_02(self):
    
        msgt('(2) Generate params for API call')
        
        f1 = CheckForExistingLayerForm(self.test_data)
        self.assertEqual(f1.is_valid(), True)
        

        msg('(a) Generate API call params')        
        self.assertEqual(f1.get_api_params_with_signature(), self.expected_params)

        msg('(b) Validate params in fresh form')
        f2 = CheckForExistingLayerForm(self.expected_params)
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
        msgt('(3) Try with HttpRequest - POST')
        
        msg('(a) Try form with HttpRequest object')
        h = HttpRequest()
        h.POST = self.expected_params
        
        f1 = CheckForExistingLayerForm(h.POST)
        self.assertEqual(f1.is_valid(), True)
        
        msg('(b) Try signature validity check - break assertion by sending dict, not HttpRequest')
        self.assertRaises(AssertionError, f1.is_signature_valid_check_post, h.POST)
            
            
        msg('(c) Try signature check with invalid data--no signature key')
        h_bad_data = HttpRequest()
        h_bad_data.POST = self.test_data 
        self.assertEqual(f1.is_signature_valid_check_post(h_bad_data), False)

        msg('(d) Try signature check with invalid data--bad signature key')
        h_bad_data2 = HttpRequest()
        h_bad_data2.POST = self.expected_params_bad_signature
        self.assertEqual(f1.is_signature_valid_check_post(h_bad_data2), False)

        msg('(e) Try signature check with valid data')
        self.assertEqual(f1.is_signature_valid_check_post(h), True)
        
        msg('(f) cleaned data.')
        self.assertEqual(f1.cleaned_data, self.expected_clean_data)
        

    @unittest.skip("skipping")
    def test_workflow_04(self):
        msgt('(4) Try with HttpRequest - GET')

        msg('(a) Try form with HttpRequest object')
        h = HttpRequest()
        h.GET = self.expected_params

        f1 = CheckForExistingLayerForm(h.GET)
        self.assertEqual(f1.is_valid(), True)

        msg('(b) Try signature validity check - break assertion by sending dict, not HttpRequest')
        self.assertRaises(AssertionError, f1.is_signature_valid_check_get, h.GET)


        msg('(c) Try signature check with invalid data--no signature key')
        h_bad_data = HttpRequest()
        h_bad_data.GET = self.test_data 
        self.assertEqual(f1.is_signature_valid_check_get(h_bad_data), False)

        msg('(d) Try signature check with invalid data--bad signature key')
        h_bad_data2 = HttpRequest()
        h_bad_data2.GET = self.expected_params_bad_signature
        self.assertEqual(f1.is_signature_valid_check_get(h_bad_data2), False)

        msg('(e) Try signature check with valid data')
        self.assertEqual(f1.is_signature_valid_check_get(h), True)

        msg('(f) cleaned data.')
        self.assertEqual(f1.cleaned_data, self.expected_clean_data)

"""        
# to run from GeoConnect
import requests

from shared_dataverse_information.dataverse_info.forms_existing_layer import CheckForExistingLayerForm
from shared_dataverse_information.dataverse_info.forms_api_validate import SIGNATURE_KEY
from shared_dataverse_information.dataverse_info.tests.msg_util import *
from django.conf import settings

data = dict( datafile_id=85\
            , dataverse_installation_name='harvard dataverse'
            )
f1 = CheckForExistingLayerForm(data)
params = None
if f1.is_valid():
    params = f1.get_api_params_with_signature()


params
"""
