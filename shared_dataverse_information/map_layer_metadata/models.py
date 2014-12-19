from django.db import models
from django.conf import settings

KEY_MAPPING_FOR_DATAVERSE_API = { 'worldmap_username' : 'worldmapUsername'\
                                    , 'layer_name' : 'layerName'\
                                    , 'layer_link' : 'layerLink'\
                                    , 'embed_map_link' : 'embedMapLink'\
                                    , 'datafile_id': 'datafileID'\
                                    , 'dv_session_token' : settings.DATAVERSE_TOKEN_KEYNAME\
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
    datafile_id = models.IntegerField(default=-1, help_text='id in database')

    dv_session_token = models.CharField(max_length=255, blank=True)


    def __unicode__(self):
        return '%s (file: %s; user: %s )' % (self.layer_name, self.datafile_id, self.worldmap_username)

    class Meta:
        abstract = True
        verbose_name_plural = 'Map Layer Metadata'
