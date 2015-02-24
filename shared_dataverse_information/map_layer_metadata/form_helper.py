

def format_to_len255(link_val):
    """
    Attempt to reduce the map_image_link if len(map_image_link) > 255 chars
    
    Example of long map_image_link:
     http://worldmap.harvard.edu/download/wms/21474/png?layers=geonode%3Asocial_disorder_in_boston_yqh_zip_9hu&width=655&bbox=-71.1914644962%2C42.227%2C-70.98616%2C42.3994625741&service=WMS&format=image%2Fpng&srs=EPSG%3A4326&request=GetMap&height=550
          
    """
    assert link_val is not None, 'link_val cannot be None'
    
    if len(link_val) <= 255:
        return link_val
    
    # Try some simple replaces to reduce it below 255
    #
    basic_replaces = {   '%2C' : ','\
                        , '%3A' : ':'\
                        , '%2F' : '/'\
                    }
                    
    for k, v in basic_replaces.items():
        link_val = link_val.replace(k, v)
    
    if len(link_val) <= 255:
        return link_val

    # OK, Try truncating bounding box decimal precision
    #
    formatted_link_parts = []
    for lp in link_val.split('&'):        
        if lp.startswith('bbox='):
            lp = format_bbox_decimals(v)
        formatted_link_parts.append(lp)
        
    shortened_url = '&'.join(formatted_link_parts)  
    if len(link_val) <= 255:
        return shortened_url

    # TO FIX: Just truncate it (temporary until dv db is updated)
    return shortened_url[:255]

    
def format_bbox_decimals(s):
    assert s is not None, "s cannot be None"
    return s
    