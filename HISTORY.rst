.. :changelog:

Release History
---------------


0.2.9 (2015-02-03)
++++++++++++++++++

**Updates**
- Update ClassifyLayerForm so it may be used for Geoconnect


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