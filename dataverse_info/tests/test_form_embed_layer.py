from __future__ import print_function
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from os.path import abspath, dirname, isfile, join
from django.test import TestCase
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
                    )
        self.expected_params = {'datafile_id': 960, 'dv_user_id': 321, 'SIGNATURE_KEY': '0f2246e1b7d0355f40b257dbe10d16afcdd2d6ece92d54d0d8843402'}
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
        self.assertEqual(f1.is_signature_valid(valid_signature), True)
        
        msg('(e) cleaned data')
        self.assertEqual(f1.cleaned_data, {'datafile_id': 960, 'dv_user_id': 321})

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
        
        msg('(c) Check signature validity.  Break assertion on signature length')
        self.assertRaises(AssertionError, f2.is_signature_valid, 'signature - not long - enough')

        msg('(d) Check signature validity.  Break assertion: signature is None')
        self.assertRaises(AssertionError, f2.is_signature_valid, None)
        
        msg('(e) Check signature validity.  Wrong signature')
        signature_str = '12345' * 11 
        self.assertEqual(f2.is_signature_valid(signature_str), False)
        
        msg('(f) Correct signature.')
        signature_str = '12345' * 11 
        self.assertEqual(f2.is_signature_valid(f1.get_api_signature()), True)

        msg('(g) cleaned data.')
        self.assertEqual(f2.cleaned_data, {'datafile_id': 960, 'dv_user_id': 321})
        
