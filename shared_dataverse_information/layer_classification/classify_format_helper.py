

def format_layer_name_for_classification(layer_name):
    """
    "geonode:my_layer_name" becomes "my_layer_name"
    "my_layer_name" stays "my_layer_name"
    """
    
    assert layer_name is not None, '"layer_name" cannot be None'
    assert len(layer_name) > 0, '"layer_name" cannot be zero-length'

    return layer_name.split(':')[-1]
