from django.db import models


# From MimeTypeDisplay.properties in the Dataverse repository
# From: https://github.com/IQSS/dataverse/blob/master/src/main/java/MimeTypeDisplay.properties

# Shapefile
CONTENT_TYPE_SHAPEFILE = 'application/zipped-shapefile'

# Recognized tabular data
CONTENT_TYPE_TAB_DELIMITED = 'text/tab-separated-values'
CONTENT_TYPE_CSV = 'text/csv'
CONTENT_TYPE_MS_EXCEL_XLS = 'application/vnd.ms-excel'
CONTENT_TYPE_MS_EXCEL_XLSX = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

TABULAR_TYPES = ('CONTENT_TYPE_TAB_DELIMITED' \
                , 'CONTENT_TYPE_CSV'\
                , 'CONTENT_TYPE_MS_EXCEL'\
                , 'CONTENT_TYPE_MS_EXCEL_XLSX'\
                )


class DataverseInfo(models.Model):
    """
    If a map layer is created using a dataverse file, this objects contains Dataverse specific information regarding that file.
    
    In addition to supplying metadata, it can also be used to identify which Layers were created using Dataverse files.
    """
    #-------------------------
    # dv user who created layer
    #-------------------------
    dv_user_id = models.IntegerField(db_index=True)
    dv_username = models.CharField(max_length=255)
    dv_user_email = models.EmailField()

    #-------------------------
    # Urls back to dataverse
    #-------------------------
    return_to_dataverse_url = models.URLField(max_length=255, blank=True)
    datafile_download_url = models.URLField(max_length=255)
    
    #-------------------------
    # dataverse info
    #-------------------------
    dataverse_installation_name = models.CharField(max_length=255, default='Harvard Dataverse', help_text='url to Harvard Dataverse, Odum Institute Dataverse, etc')
    dataverse_id = models.IntegerField(default=-1, help_text='id in database')
    dataverse_name = models.CharField(max_length=255, db_index=True)
    dataverse_description = models.TextField(blank=True) 
    
    #-------------------------
    # dataset info
    #-------------------------
    dataset_id = models.IntegerField(default=-1, help_text='id in database')  # for API calls.  
    
    #-------------------------
    # dataset version info
    #-------------------------
    dataset_version_id = models.IntegerField(default=-1, help_text='id in database')  # for API calls.
    dataset_semantic_version = models.CharField(max_length=25, help_text='example: "DRAFT",  "1.2", "2.3", etc', blank=True)  # for API calls.
    dataset_name = models.CharField(max_length=255, blank=True)  # for display
    dataset_citation = models.CharField(max_length=255)
    dataset_description = models.TextField(blank=True) 
    dataset_is_public = models.BooleanField()

    #-------------------------
    # datafile info
    #-------------------------
    datafile_id = models.IntegerField(default=-1, help_text='id in database', db_index=True)  # for API calls.  
    datafile_label = models.CharField(max_length=255, help_text='original file name')  
    
    datafile_expected_md5_checksum = models.CharField(max_length=100)  
    datafile_filesize = models.IntegerField(help_text='in bytes')
    datafile_content_type = models.CharField(max_length=255)
    datafile_create_datetime = models.DateTimeField()#blank=True, null=True)
            
    #-------------------------
    # timestamps
    #-------------------------
    created = models.DateTimeField(auto_now_add=True) 
    modified = models.DateTimeField(auto_now=True)
    
    
    
    def __unicode__(self):
        return '%s (%s -> %s)' % (self.datafile_label, self.dataverse_name, self.dataset_name)
        
    class Meta:
        abstract = True
        ordering = ('-modified',  )
        verbose_name_plural = 'Dataverse Info'
    