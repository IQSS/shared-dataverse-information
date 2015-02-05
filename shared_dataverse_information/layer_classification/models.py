from django.db import models

"""
These models are used in two projects:

    WorldMap - https://github.com/cga-harvard/cga-worldmap
    GeoConnect - https://github.com/iqss/geoconnect
    
The WorldMap values are considered the authoritative source of information.

"""


class ClassificationMethod(models.Model):
    """Used for the GeoConnect style classification tools 
    """
    display_name = models.CharField(max_length=255)
    value_name = models.CharField(max_length=100, unique=True, help_text='Parameter value in the the geoserver api calls')
    is_string_usable = models.BooleanField(default=False)

    sort_order = models.IntegerField(default=10, help_text='display order for user')
    active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True) 
    modified = models.DateTimeField(auto_now=True)
    
    
    def __unicode__(self):
        return  '%s (%s)' % (self.display_name, self.value_name)

    class Meta:
        ordering = ('sort_order', 'display_name')
        

class ColorRamp(models.Model):
    """Used for the GeoConnect style classification tools 
    
    Note: value names maybe the same--e.g., Custom can have different display names with specific start/end colors
    """
    display_name = models.CharField(max_length=255, unique=True)
    value_name = models.CharField(max_length=100, help_text='Parameter value in the the geoserver api calls')
    sort_order = models.IntegerField(default=10, help_text='display order for user')
    start_color = models.CharField(max_length=30, blank=True, help_text='hex color with "#", as in "#ffcc00"')
    end_color = models.CharField(max_length=30, blank=True, help_text='hex color with "#", as in "#ffcc00"')
    active = models.BooleanField(default=True)
    
    created = models.DateTimeField(auto_now_add=True) 
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return  '%s (%s)' % (self.display_name, self.value_name)

    class Meta:
        ordering = ('sort_order', 'display_name')
        
        
class ClassifyRequestData(models.Model):
    """
    Abstract class.  Main use is to create a form using APIValidateHelperForm
    """
    datafile_id = models.IntegerField()
    dataverse_installation_name = models.CharField(max_length=255)

    layer_name = models.CharField(max_length=255)
    attribute = models.CharField(max_length=255)

    intervals = models.IntegerField()
    method = models.CharField(max_length=255)

    ramp = models.CharField(max_length=255)
    startColor = models.CharField(max_length=30)
    endColor = models.CharField(max_length=30)

    reverse = models.BooleanField(default=False)

    class Meta:
        abstract = True

