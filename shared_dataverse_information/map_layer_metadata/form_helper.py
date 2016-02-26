from decimal import Decimal

def format_to_len255(link_val):
    """
    Attempt to reduce the map_image_link if len(map_image_link) > 255 chars

    Example of long map_image_link:
     http://worldmap.harvard.edu/download/wms/21474/png?layers=geonode%3Asocial_disorder_in_boston_yqh_zip_9hu&width=655&bbox=-71.1914644962%2C42.227%2C-70.98616%2C42.3994625741&service=WMS&format=image%2Fpng&srs=EPSG%3A4326&request=GetMap&height=550

    """
    assert link_val is not None, 'link_val cannot be None'

    # Try some simple replaces to reduce it below 255
    #
    basic_replaces = {   '%2C' : ','\
                        , '%3A' : ':'\
                        , '%2F' : '/'\
                    }

    for k, v in basic_replaces.items():
        link_val = link_val.replace(k, v)

    #print 'check 1', link_val
    # OK, Try truncating bounding box decimal precision
    #
    formatted_link_parts = []
    for lp in link_val.split('&'):
        if lp.startswith('bbox='):
            lp = format_bbox_decimals(lp)
        formatted_link_parts.append(lp)

    shortened_url = '&'.join(formatted_link_parts)
    if len(link_val) <= 255:
        return shortened_url

    # TO FIX: Just truncate it (temporary until dv db is updated)
    return shortened_url[:255]


def format_bbox_decimals(bbox_str):
    """
    Example:
        in: bbox=-71.1914644962,42.2272481395,-70.9861620286,42.3994625741
        out: bbox=-71.1914,42.2272,-70.9861,42.3994
    """
    assert bbox_str is not None, "bbox_str cannot be None"
    assert bbox_str.startswith('bbox='), "bbox_str must start with 'bbox='"

    attr_val = bbox_str.split('=')
    if not len(attr_val) == 2:  # Expected 2 vals, return str
        return bbox_str

    bbox_attr, bbox_val = attr_val
    fmt_vals = []
    for decimal_str in bbox_val.split(','):
        try:
            fmt_vals.append('%.4f' % Decimal(decimal_str))
        except:
            fmt_vals.append(decimal_str)

    fmt_bbox_str =  '%s=%s' % (bbox_attr, ','.join(fmt_vals))

    return fmt_bbox_str
