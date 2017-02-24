from django import VERSION as django_version


def can_use_fields_all():
    """
    For forms, all fields are often used.
    In Django 1.4, no params need to be specified.
    In later versions, specify the META param:
        fields = '__all__'

    Needs to Work in Django 1.4.13 (WorldMap) and 1.9+ (Geoconnect)
    """
    if django_version[0] <= 1 and django_version[1] < 7:
        return False
    return True
