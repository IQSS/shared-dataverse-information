from django.conf import settings

"""
URLs for APIS used to contact the WorldMap

"""

def format_worldmap_api_url(url_path):
    
    assert url_path is not None, "url path cannot be None"
    
    formatted_url = '/'.join(s for s in (settings.WORLDMAP_SERVER_URL.strip('/'), url_path.lstrip('/')))

    return formatted_url


# shapefile import API
#
ADD_SHAPEFILE_API_PATH = format_worldmap_api_url('/dataverse/import-shapefile/')


# Delete dataverse-created map layer
#
DELETE_LAYER_API_PATH = format_worldmap_api_url('/dataverse/delete-map-layer/')


# classify layer API
#
CLASSIFY_LAYER_API_PATH = format_worldmap_api_url('/dataverse/classify-layer/')


# classify layer API
#
GET_CLASSIFY_ATTRIBUTES_API_PATH = format_worldmap_api_url('/dataverse/get-classify-attributes/')



# Get existing layer by Dataverse installation name and Dataverse file id
#
GET_LAYER_INFO_BY_DATAVERSE_INSTALLATION_AND_FILE_API_PATH = format_worldmap_api_url('/dataverse-layer/get-existing-layer-info/')


# check for existing layer
#
CHECK_FOR_EXISTING_LAYER_API_PATH = format_worldmap_api_url('/dataverse/check-for-existing-layer/')



#
#
#GET_VIEW_PRIVATE_LAYER_URL = format_worldmap_api_url('dataverse-private-layer/request-private-layer-url/')
