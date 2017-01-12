from django.db import models
from django.conf import settings

# ------------------------------------------------------
# Set DATAVERSE_TOKEN_KEYNAME
# ------------------------------------------------------
dataverse_token_name = 'no-token'
if hasattr(settings, 'DATAVERSE_TOKEN_KEYNAME'):
    dataverse_token_name = settings.DATAVERSE_TOKEN_KEYNAME
assert dataverse_token_name is not None, "dataverse_token_name cannot be None"

# ------------------------------------------------------
# Set WORLDMAP_SERVER_URL and WORLDMAP_SERVER_URL_BASE
# ------------------------------------------------------
WORLDMAP_SERVER_URL = 'http://worldmap.harvard.edu'
if hasattr(settings, 'WORLDMAP_SERVER_URL'):
    WORLDMAP_SERVER_URL = settings.WORLDMAP_SERVER_URL
assert WORLDMAP_SERVER_URL is not None, "WORLDMAP_SERVER_URL cannot be None"

# Used for forcing https
WORLDMAP_SERVER_URL_BASE = WORLDMAP_SERVER_URL.split('//')[-1].lower()  # e.g. worldmap.harvard.edu



KEY_MAPPING_FOR_DATAVERSE_API = { 'worldmap_username' : 'worldmapUsername',
                                'layer_name' : 'layerName',
                                'layer_link' : 'layerLink',
                                'embed_map_link' : 'embedMapLink',
                                'dv_session_token' : dataverse_token_name,
                                'map_image_link' : 'mapImageLink',
                                'llbbox' : 'LatLngBoundingBox',
                                'download_links' : 'mapLayerLinks',
                                #, 'attribute_info' : 'attribute_info'  # not yet used by dataverse
                                }
DATAVERSE_REQUIRED_KEYS = KEY_MAPPING_FOR_DATAVERSE_API.values()

class MapLayerMetadata(models.Model):
    """
    Map layer metadata from Worldmap  stored in Dataverse
    """
    worldmap_username = models.CharField(max_length=255)
    layer_name = models.CharField(max_length=255)

    layer_link = models.URLField(max_length=255)
    embed_map_link = models.URLField(max_length=255)
    #datafile_id = models.IntegerField(default=-1, help_text='id in database')

    llbbox = models.CharField('Lat/Lng bounding box', max_length=255, blank=True)
    attribute_info = models.TextField('attribute names|types|display names')
    download_links = models.TextField('download data links', blank=True)
    map_image_link = models.TextField('map image link--sometimes exceeds 255 chars')
    dv_session_token = models.CharField(max_length=255, blank=True)



    def __unicode__(self):
        return '%s (user: %s )' % (self.layer_name, self.worldmap_username)

    class Meta:
        abstract = True
        verbose_name_plural = 'Map Layer Metadata'
