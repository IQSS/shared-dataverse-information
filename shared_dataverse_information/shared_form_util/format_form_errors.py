"""
If a form is not valid, format the errors for a string
"""
from django import forms

def format_errors_as_text(form_obj):
    """
    Format Django form errors as text.

    RAW:
        {'dv_user_email': [u'This field is required.'], 'abstract': [u'This field is req
uired.'], 'shapefile_name': [u'This field is required.'], 'title': [u'This field
 is required.']}

    FORMATTED:
    '''
    Errors found with the following field(s):

    - dv_user_email: This field is required.

    - abstract: This field is required.

    - shapefile_name: This field is required.

    - dv_user_email: This is not a valid email address.
    '''
    :param form_obj: forms.Form, forms.ModelForm, is_valid() is False
    :return: str
    """
    assert isinstance(form_obj, forms.Form) or isinstance(form_obj, forms.ModelForm) \
        , "form_obj must be a forms.Form or a forms.ModelForm"

    assert form_obj.is_valid() is False, "The form is valid.  Expecting an invalid form with errors."

    outlines = ['Errors found with the following field(s):']

    for field_name, err_list in form_obj.errors.items():
        for idx, err_msg in enumerate(err_list):
            if idx == 0:
                outlines.append('\n- %s: %s' % (field_name, err_msg))
            else:
                outlines.append('\t\t%s' % (err_msg))

    return '\n'.join(outlines)


