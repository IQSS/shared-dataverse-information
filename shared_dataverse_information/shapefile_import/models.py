from django.db import models

"""
Abstract model used as a template for:
    - GeoConnect sending a shapefile to WorldMap
    - WorldMap validating info sent from GeoConnect

Note: This is factoring out some of the original import code
"""

class ShapefileImportData(models.Model):

    # required
    title = models.CharField(max_length=255)
    abstract = models.TextField()
    dv_user_email = models.EmailField('Dataverse user email')
    shapefile_name = models.CharField(max_length=255)

    # optional
    keywords = models.CharField(max_length=255, blank=True)
    worldmap_username = models.CharField(max_length=100, blank=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return '%s (%s)' % (self.title, self.shapefile_name)

