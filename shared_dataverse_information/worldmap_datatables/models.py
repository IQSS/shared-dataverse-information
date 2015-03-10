from django.db import models


TABLE_JOIN_TO_RESULT_MAP = dict(tablejoin_id='pk'\
                        , tablejoin_view_name='view_name'\
                        , join_layer_id='join_layer.id'\
                        , join_layer_typename='join_layer.typename'\
                        , join_layer_url='join_layer.get_absolute_url'\
                        , matched_record_count='matched_records_count'\
                        , unmatched_record_count='unmatched_records_count'\
                        , unmatched_records_list='unmatched_records_list'\
                        , table_name='datatable.table_name'\
                        , table_join_attribute='table_attribute.attribute'\
                        , layer_typename='join_layer.typename'\
                        , layer_join_attribute='layer_attribute.attribute'\
    )

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


    """

     'join_id': tj.pk,
                    'view_name': tj.view_name,
                    'matched_records': tj.matched_records_count,
                    'unmatched_records': tj.unmatched_records_count,
                    'unmatched_records_list': tj.unmatched_records_list,
                    'datatable': tj.datatable.table_name,
                    'source_layer': tj.source_layer.typename,
                    'table_attribute': tj.table_attribute.attribute,
                    'layer_attribute': tj.layer_attribute.attribute,
                    'join_layer': tj.join_layer.typename,
                    'layer_url': tj.join_layer.get_absolute_url()
    """