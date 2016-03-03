from django.conf import settings

"""
URLs for APIS used to contact the WorldMap

"""

def format_worldmap_api_url(url_path):

    assert url_path is not None, "url path cannot be None"

    formatted_url = '/'.join(s for s in \
        (settings.WORLDMAP_SERVER_URL.strip('/'), url_path.lstrip('/')))

    return formatted_url


# shapefile import API
#
ADD_SHAPEFILE_API_PATH = format_worldmap_api_url('/dataverse/api/import-shapefile/')


# Delete dataverse-created map layer
#
DELETE_LAYER_API_PATH = format_worldmap_api_url('/dataverse/api/delete-map-layer/')


# classify layer API
#
CLASSIFY_LAYER_API_PATH = format_worldmap_api_url('/dataverse/api/classify-layer/')


# classify layer API
#
GET_CLASSIFY_ATTRIBUTES_API_PATH = format_worldmap_api_url('/dataverse/api/get-classify-attributes/')



# Get existing layer by Dataverse installation name and Dataverse file id
#
GET_LAYER_INFO_BY_DATAVERSE_INSTALLATION_AND_FILE_API_PATH = \
    format_worldmap_api_url('/dataverse/api/layer-info/')


# check for existing layer
#
#CHECK_FOR_EXISTING_LAYER_API_PATH = format_worldmap_api_url('/dataverse/api/check-for-existing-layer/')

#
#
#GET_VIEW_PRIVATE_LAYER_URL = format_worldmap_api_url('dataverse-private-layer/request-private-layer-url/')

#
# Datatables: Retrieve potential datatable JoinTargets
GET_JOIN_TARGETS = format_worldmap_api_url('/datatables/api/jointargets/')

#
# Datatables: Join table to JoinTarget
UPLOAD_JOIN_DATATABLE_API_PATH = format_worldmap_api_url('dataverse/api/tabular/upload-join/')

#
# Retrieve existing table join info - /datatables/api/join/(?P<tj_id>\d+)
GET_TABLEJOIN_INFO = format_worldmap_api_url('/datatables/api/join/')

# /datatables/api/join/remove/(?P<tj_id>\d+)
DELETE_TABLEJOIN = format_worldmap_api_url('/datatables/api/join/remove/')

#
# Datatables: Map Lat/Lng table
MAP_LAT_LNG_TABLE_API_PATH = format_worldmap_api_url('/dataverse/api/tabular/upload-lat-lng/')
