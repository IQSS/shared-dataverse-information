.. :changelog:

Release History
---------------

0.3.7 (2015-03-18)
++++++++++++++++++
- Added DataTableResponse

0.3.6 (2015-03-17)
++++++++++++++++++
- Added DataTableUploadForm (+ uploaded_file field)
- Added attributes to TableUploadAndJoinRequest

0.3.5 (2015-03-13)
++++++++++++++++++
Added worldmap_datatables for geoconnect API
- Added TableJoinResult, TableJoinResultForm
- Added TableJoinRequest, TableJoinRequestForm
- Added MapLatLngLayerRequest, MapLatLngLayerRequestForm


0.3.4 (2015-03-09)
++++++++++++++++++
Added TABULAR_TYPES in the DataverseInfo model

0.3.3 (2015-02-24)
++++++++++++++++++
Use forms to reduce size of map_image_link.  Change bbox decimal precision to 4. See "def format_to_len255"

0.3.2 (2015-02-24)
++++++++++++++++++
Changed map_image_link from a URLField to a TextField.  Ran into error when the value exceeded 255 chars.

0.3.1 (2015-02-13)
++++++++++++++++++
Django req. was dropped--but this change was then reverted.

0.3.0 (2015-02-05)
++++++++++++++++++

**Updates**
- Update ClassifyRequestDataForm and LayerAttributeRequestForm to include datafile_id and dataverse_installation_name



0.2.9 (2015-02-04)
++++++++++++++++++

**Updates**
- Update ClassifyLayerForm so it may be used for Geoconnect
- ClassifyRequestDataForm form created to check classification API calls

0.2.8 (2015-02-02)
++++++++++++++++++

**Updates**
- Beginning use of APIValidateHelperForm for API calls
    - Updated to ShapefileImportDataForm to inherit from APIValidateHelperForm
    - Updated Delete function to use APIValidateHelperForm
- Remove unused EmbedLayerForm



0.2.7 (2015-01-21)
++++++++++++++++++

**Updates**
- Updated WorldMapToGeoconnectMapLayerMetadataValidationForm
    - Used clean_layer_link to point to a new map instead of the standalone layer


0.2.6 (2015-01-21)
++++++++++++++++++

**Updates**
- Updated WorldMapToGeoconnectMapLayerMetadataValidationForm
    - Set embed_map_link to https for dev and prod--so they will work in an iframe

0.2.5 (2015-01-08)
++++++++++++++++++

**Updates**
- Add worldmap_api_helper.url_helper
    - Code moved out of geoconnect

0.2.4 (2014-12-22)
++++++++++++++++++

**Updates**

- Add fields to MapLayerMetadata object
    - llbbox - lat/long bounding box
    - map_image_link - link to a png image
    - download_links - other download links for a WorldMap layer
    - download_links - dict of links to export in different formats:
        - [u'zip', u'gml', u'tiff', u'KML', u'jpg', u'json', u'pdf', u'csv', u'xls', u'png']
        - .zip is shapefile, json is geojson, tiff is geotiff
- Remove field from MapLayerMetadata object
    - datafile_id - not needed.  Field is part of the token.
        - Source data at WorldMap only needs a Layer object to produce MapLayerMetadata
- Share MapLayerMetadata object and related form code in Geoconnect and WorldMap
- added index to DataverseInfo.datafile_id