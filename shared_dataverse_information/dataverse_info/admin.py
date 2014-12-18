from django import forms
from django.contrib import admin

from .models import DataverseInfo
from .forms import DataverseInfoValidationForm


class DataverseInfoAdmin(admin.ModelAdmin):
    class Meta:
        
        abstract=True
        
    form = DataverseInfoValidationForm
    
    save_on_top = True
    search_fields = ['dv_username',  'datafile_label','dataset_name', 'dataverse_name',]# 'dv_file']
    list_display = ['datafile_id', 'dv_username',  'datafile_label', 'dataset_name', 'dataverse_name', 'modified']  # 'dv_file', 
    list_filter = [ 'dataset_is_public', 'dv_username', 'dataverse_name', 'dataset_name']   
    readonly_fields = ['modified', 'created'\
                    , 'dataverse_id', 'dataset_id', 'datafile_id'\
                    , 'datafile_filesize', 'datafile_content_type', 'datafile_expected_md5_checksum'\
                    , 'datafile_create_datetime'\
                    #, 'dataset_is_public'\
                    ]
    fieldsets = [
         ('DataFile Info', {
                  'fields': ( 'dataset_is_public'\
                  , ('datafile_label', 'datafile_id',  )\
                  , ('datafile_filesize', 'datafile_content_type')\
                  , ('datafile_create_datetime', 'datafile_expected_md5_checksum',)\
                  )
              }),
         #('Retrieved File', {
         #            'fields': ('dv_file', 'gis_scratch_work_directory' )
         # }),
         ('Dataverse user', {
               'fields': ('dv_user_email', ('dv_user_id', 'dv_username'))
           }),
           ('Dataverse', {
               'fields': ('dataverse_installation_name', \
                        ('dataverse_name', 'dataverse_id'),\
                        'dataverse_description',\
                        'return_to_dataverse_url',\
                         )
           }),
           ('Dataset Info', {
               'fields': ('dataset_id',)
           }),
           ('Dataset Version Info', {
               'fields': (('dataset_version_id', 'dataset_semantic_version',), 'dataset_name', 'dataset_citation', 'dataset_description')
           }),
           #('Session Info', {
           #       'fields': ('dv_session_token', )
           #}),          
           ('Read-Only Info', {
               'fields': (('modified', 'created') )
           }),
       ]
       


