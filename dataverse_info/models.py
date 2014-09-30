from django.db import models


        
        
class DataverseInfo(models.Model):
    """
    If a map layer is created using a dataverse file, this objects contains Dataverse specific information regarding that file.
    
    In addition to supplying metadata, it can also be used to identify which Layers were created using Dataverse files.
    """
    # dv user who created layer
    dv_username = models.CharField(max_length=255, db_index=True)
    dv_user_email = models.EmailField(db_index=True)

    # dataset url
    return_to_dataverse_url = models.URLField(max_length=255, blank=True)
    
    # dataverse info
    dataverse_installation_name = models.CharField(max_length=255, default='Harvard Dataverse', help_text='Harvard Dataverse, Odum Institute Dataverse, etc')
    dataverse_name = models.CharField(max_length=255, db_index=True)
    dataverse_description = models.TextField(blank=True) 
    
    # dataset info
    dataset_name = models.CharField(max_length=255, blank=True)  # for display
    dataset_description = models.TextField(blank=True) 

    dataset_id = models.IntegerField(default=-1, help_text='id in database')  # for API calls.  
    dataset_version_id = models.IntegerField(default=-1, help_text='id in database')  # for API calls.

    dataset_semantic_version = models.CharField(max_length=25, help_text='example: 1.2, 2.3, etc', blank=True)  # for API calls.
    doi = models.CharField('DOI', max_length=255, blank=True)
    citation = models.CharField(max_length=255, blank=True)

    # datafile info
    datafile_label = models.CharField(max_length=255, help_text='original file name')  
    datafile_description = models.TextField(blank=True)   
        
    # timestamps
    created = models.DateTimeField(auto_now_add=True) 
    modified = models.DateTimeField(auto_now=True)
    
    
    
    def __unicode__(self):
        return '%s (%s -> %s)' % (self.datafile_label, self.dataverse_name, self.dataset_name)
        
    class Meta:
        abstract = True
        ordering = ('-modified',  )
        verbose_name_plural = 'Dataverse Info'
    