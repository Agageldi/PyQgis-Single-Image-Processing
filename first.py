import qgis.core

#get Rasterr layer
#now it i not the best way to do
rlayer = qgis.utils.iface.activeLayer()

#getting sample from raster
#identity() object
ident = rlayer.dataProvider().identify(QgsPoint(100,-100),QgsRaster.IdentifyFormatValue)
sampleValue = ident.results()

#gdal import
gtif=gdal.Open("/home/user/thesis/IMG_0048_4.tif")

