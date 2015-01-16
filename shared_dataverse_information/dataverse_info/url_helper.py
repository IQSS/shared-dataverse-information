
DEFAULT_SERVER_NAME = 'https://dvn-build.hmdc.harvard.edu/'

def format_api_url(server_name, url_path):    
    assert server_name is not None, "server_name cannot be None.  (It can be an empty string '')"
    assert url_path is not None, "url_path cannot be None"
    #
    return '/'.join(s for s in [server_name.rstrip('/'), url_path.lstrip('/')] )




def get_api_url_update_map_metadata(server_name=DEFAULT_SERVER_NAME):
    """
    Return the Dataverse API path for adding/updating map layer metadata
    """
    assert server_name is not None, "server_name cannot be None.  (It can be an empty string '')"
    #
    return format_api_url(server_name, '/api/worldmap/update-layer-metadata')
    
    
def get_api_url_delete_metadata(server_name=DEFAULT_SERVER_NAME):
    """
    Return the Dataverse API path for deleting a metadata
    """
    assert server_name is not None, "server_name cannot be None.  (It can be an empty string '')"
    #
    return format_api_url(server_name, '/api/worldmap/delete-layer-metadata/')
    

    
def get_api_url_delete_token(server_name=DEFAULT_SERVER_NAME):
    """
    Return the Dataverse API path for deleting a token
    """
    assert server_name is not None, "server_name cannot be None.  (It can be an empty string '')"
    #
    return format_api_url(server_name, '/api/worldmap/delete-token/')
    
    