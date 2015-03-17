#   Delimiter choices
#   For each delimiter, specify a "varname", "value", and "friendly_name"
#
DELIMITER_TYPE_INFO = ( dict(varname='COMMA', value=',', friendly_name='Comma Separated (.csv)'),
                        dict(varname='TAB', value='\t', friendly_name='Tab Separated (.tab)'),
                    )
                    
assert len(DELIMITER_TYPE_INFO) > 1, "DELIMITER_TYPE_INFO must have at least one value"

DELIMITER_TYPE_CHOICES = [ (dt['varname'], dt['friendly_name']) for dt in DELIMITER_TYPE_INFO] # choices for Form

DELIMITER_VALUE_LOOKUP = dict( (dt['varname'], dt['value']) for dt in DELIMITER_TYPE_INFO)  # value look up for form "clean"

DELIMITER_VALUES = [ dt['value'] for dt in DELIMITER_TYPE_INFO ] 

DEFAULT_DELIMITER = DELIMITER_TYPE_INFO[0]['varname']   # form default value

def format_delimiter(delim):
    
    if delim is None or len(delim) == 0:
        return DEFAULT_DELIMITER
        
    if len(delim) > 1:
        delim = delim[0]
        
    if delim in DELIMITER_VALUES:
        return delim
        
    return None
