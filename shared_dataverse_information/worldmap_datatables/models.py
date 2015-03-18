from django.contrib.auth.models import User
from django.db import models


TABLE_JOIN_TO_RESULT_MAP = dict(tablejoin_id='pk',
                             tablejoin_view_name='view_name',
                             join_layer_id='join_layer.id',
                             join_layer_typename='join_layer.typename',
                             join_layer_url='join_layer.get_absolute_url',
                             matched_record_count='matched_records_count',
                             unmatched_record_count='unmatched_records_count',
                             unmatched_records_list='unmatched_records_list',
                             table_id='datatable.id',
                             table_name='datatable.table_name',
                             table_join_attribute='table_attribute.attribute',
                             layer_typename='join_layer.typename',
                             layer_join_attribute='layer_attribute.attribute')



class TableUploadAndJoinRequest(models.Model):

    title = models.CharField(max_length=255, help_text='Title for New DataTable')
    abstract = models.TextField(default='(no abstract)')
    delimiter = models.CharField(max_length=10, default=',')

    uploaded_file = models.FileField(upload_to='datatables/%Y/%m/%d')

    no_header_row = models.BooleanField(default=False,
            help_text='Specify "True" if the first row is not a header')

    table_attribute = models.CharField(max_length=255,
                                     help_text='DataTable attribute name to join on')
    layer_typename = models.CharField(max_length=255, help_text='Layer name')
    layer_attribute = models.CharField(max_length=255,
                                    help_text='Layer attribute name to join on')

    new_layer_owner = models.ForeignKey(User, blank=True, null=True, help_text='Optional owner')

    def __unicode__(self):
        return 'DataTable: %s to Layer: %s.%s)'\
                % (self.title\
                    , self.layer_typename\
                    , self.layer_attribute\
                )

    class Meta:
        abstract = True

class DataTableResponse(models.Model):
    """
    Used for the Worldmap API responses
    """
    id = models.IntegerField()
    title = models.CharField(max_length=255)
    abstract = models.TextField(blank=True)
    delimiter = models.CharField(max_length=6, default='')
    #owner = models.ForeignKey(User, blank=True, null=True)
    table_name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title

    class Meta:
        abstract=True



class MapLatLngLayerRequest(models.Model):
    """
    Used for the Worldmap API request
    """
    title = models.CharField(max_length=255, help_text='Title for New DataTable')
    abstract = models.TextField(default='(no abstract)')

    delimiter = models.CharField(max_length=10, default=',')
    uploaded_file = models.FileField(upload_to='datatables/%Y/%m/%d')
    no_header_row = models.BooleanField(default=False,
            help_text='Specify "True" if the first row is not a header')

    lng_attribute = models.CharField(max_length=255, help_text='Longitude column name')
    lat_attribute = models.CharField(max_length=255, help_text='Latitude column name')

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True

class MapLatLngLayerResult(models.Model):
    """
    Information returned after a successful mapping of a lat/lng layer
    """
    tablejoin_id = models.IntegerField(help_text='TableJoin pk')

    tablejoin_view_name = models.CharField(max_length=255, help_text='TableJoin view_name')

    # New Join Layer
    #
    layer_id = models.CharField(max_length=255\
                        , help_text='Layer id')

    layer_typename = models.CharField(max_length=255\
                        , help_text='Layer typename')

    layer_url = models.CharField(max_length=255\
                        , help_text='layer.get_absolute_url()')


    mapped_record_count = models.IntegerField(default=0, help_text='TableJoin matched_records_count')
    unmapped_record_count = models.IntegerField(default=0, help_text='TableJoin unmatched_records_count')
    unmapped_records_list = models.TextField(blank=True, help_text='TableJoin unmatched_records_list')

    table_name = models.CharField(max_length=255, help_text='TableJoin datatable.table_name')
    table_join_attribute = models.CharField(max_length=255\
                        , help_text='TableJoin table_attribute.attribute')

    layer_typename = models.CharField(max_length=255, help_text='TableJoin join_layer.typename')
    layer_join_attribute = models.CharField(max_length=255\
                        , help_text='TableJoin layer_attribute.attribute')


    def __unicode__(self):
        return self.join_layer_typename

    class Meta:
        abstract = True



class TableJoinRequest(models.Model):

    table_name = models.CharField(max_length=255, help_text='DataTable name')
    table_attribute = models.CharField(max_length=255\
                                    , help_text='DataTable attribute name to join on')

    layer_typename = models.CharField(max_length=255, help_text='Layer name')
    layer_attribute = models.CharField(max_length=255\
                                    , help_text='Layer attribute name to join on')

    new_layer_owner = models.ForeignKey(User, blank=True, null=True, help_text='Optional owner')

    def __unicode__(self):
        return 'DataTable: (%s.%s) to Layer: (%s.%s)'\
                % (self.table_name\
                    , self.table_attribute\
                    , self.layer_typename\
                    , self.layer_attribute\
                )

    class Meta:
        abstract = True


class TableJoinResult(models.Model):
    """
    Information returned after a successful table join
    """
    tablejoin_id = models.IntegerField(help_text='TableJoin pk')

    tablejoin_view_name = models.CharField(max_length=255, help_text='TableJoin view_name')

    # New Join Layer
    #
    join_layer_id = models.CharField(max_length=255\
                        , help_text='TableJoin join_layer.id')

    join_layer_typename = models.CharField(max_length=255\
                        , help_text='TableJoin join_layer.typename')

    join_layer_url = models.CharField(max_length=255\
                        , help_text='TableJoin join_layer.get_absolute_url()')


    matched_record_count = models.IntegerField(default=0, help_text='TableJoin matched_records_count')
    unmatched_record_count = models.IntegerField(default=0, help_text='TableJoin unmatched_records_count')
    unmatched_records_list = models.TextField(blank=True, help_text='TableJoin unmatched_records_list')

    table_id = models.IntegerField(help_text='TableJoin datatable.id')
    table_name = models.CharField(max_length=255, help_text='TableJoin datatable.table_name')
    table_join_attribute = models.CharField(max_length=255\
                        , help_text='TableJoin table_attribute.attribute')

    layer_typename = models.CharField(max_length=255, help_text='TableJoin join_layer.typename')
    layer_join_attribute = models.CharField(max_length=255\
                        , help_text='TableJoin layer_attribute.attribute')


    def __unicode__(self):
        return self.join_layer_typename

    class Meta:
        abstract = True


