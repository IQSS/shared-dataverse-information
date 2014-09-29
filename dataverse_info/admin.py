from django.contrib import admin

from dataverse_info.models import DataverseInfo


class DataverseInfoAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('map_layer__name',  'dataverse_name', 'dataset_name', 'datafile_label', 'dataset_description')
    list_display = ('map_layer', 'dataset_name', 'doi', 'datafile_label', 'dataverse_name', )
    list_filter = ('dataverse_name', )   
    readonly_fields = ('modified', 'created')
admin.site.register(DataverseInfo, DataverseInfoAdmin)

