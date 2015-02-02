from __future__ import print_function
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from os.path import abspath, dirname, isfile, join
from django.test import TestCase
from shared_dataverse_information.dataverse_info.models import DataverseInfo
from shared_dataverse_information.dataverse_info.forms import DataverseInfoValidationForm
from shared_dataverse_information.dataverse_info.forms_existing_layer import CheckForExistingLayerForm

from shared_dataverse_information.dataverse_info.tests.msg_util import *

import unittest
import json


class ValidationFormTest(TestCase):
    
    def setUp(self): 
        test_data_file = join( dirname(dirname(abspath(__file__)))\
                                , 'fixtures'\
                                , 'dataverse_info_test_fixtures_01.json'\
                            )
        if not isfile(test_data_file):
            raise ValueError('File not found: %s' % test_data_file)
            
        self.test_data = json.loads(open(test_data_file, 'r').read())
                       
                    
    def test_form_validation1(self):
    
        msgt('(1) Test valid data')
        
        validation_form = DataverseInfoValidationForm(self.test_data)
        #print 'valid',validation_form.is_valid()
        self.assertEqual(validation_form.is_valid(), True)

    def test_form_validation2(self):

        msgt('(2) Test invalid data')

        tdata = self.test_data.copy()
        tdata['dataset_id'] = '11z'
        tdata['return_to_dataverse_url'] = 'ha'
        #msg(tdata)
        validation_form = DataverseInfoValidationForm(tdata)
        #msg('valid: %s' % validation_form.is_valid())
        self.assertEqual(validation_form.is_valid(), False)

        msg('check for attributes in error')
        err_keys = validation_form.errors.keys()
        msg(err_keys)        
        self.assertEqual('return_to_dataverse_url' in err_keys, True)
        self.assertEqual('dataset_id' in err_keys, True)
        
        msg('check for err messages')
        err_msgs = validation_form.errors.values()
        msg(err_msgs)
        self.assertEqual([u'Enter a valid URL.'] in err_msgs, True)
        self.assertEqual([u'Enter a whole number.'] in err_msgs, True)
    
    #@unittest.skip("demonstrating skipping")
    def test_form_validation3(self):
        
        msgt('(3) Test valid data with extra fields.  Are the extra fields removed?')
        
        # retrieve data and add extra fields
        tdata = self.test_data.copy()
        tdata.update({ 'map_layer' : 'extra field 1'\
                    , 'comment' : 'extra field 2'\
                    , 'token_check' : 'extra field 3'\
                })

        validation_form = DataverseInfoValidationForm(tdata)
        msg ('is valid: %s' % validation_form.is_valid())
        err_msgs = validation_form.errors.values()
        msg('errs: %s' % err_msgs)
    
        self.assertEqual(validation_form.is_valid(), True)
        
        cleaned_data = validation_form.cleaned_data
        self.assertEqual(cleaned_data.has_key('map_layer'), False)
        self.assertEqual(cleaned_data.has_key('comment'), False)
        self.assertEqual(cleaned_data.has_key('token_check'), False)
        
        msg('Yes, strips out the extra fields?')
        #msg(cleaned_data)
        
        #dvinfo_obj = validation_form.save(commit=False)
        #self.assertEqual(type(dvinfo_obj), DataverseInfo)
        #msg('yes, converts into a DataverseInfo object (minus the map_layer)')
        