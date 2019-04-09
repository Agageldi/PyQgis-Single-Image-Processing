from osgeo import gdal, osr
import math

src_filename ='/home/user/thesis/IMG_0048_4.tif'
dst_filename = '/home/user/thesis/output.tif'

# Opens source dataset
src_ds = gdal.Open(src_filename)
format = "GTiff"
driver = gdal.GetDriverByName(format)

# Open destination dataset
dst_ds = driver.CreateCopy(dst_filename, src_ds, 0)


# Specify raster location through geotransform array
# (uperleftx, scalex, skewx, uperlefty, skewy, scaley)
# Scale = size of one pixel in units of raster projection
# this example below assumes 100x100
ex = myEXIFdata(src_filename)
coor = ex["gps"]
Radius = 6371000.
fh = 50.

dx=89.04573706*fh/100
dy=66.9190639*fh/100

rx=ex["size"][0]
ry=ex["size"][1]

width  = math.degrees(dx/(Radius*math.cos(math.radians(coor[0])) ))
height = -math.degrees(dy/Radius)

x_scale = width/rx
y_scale = height/ry

alpha = 45
x_skew = -math.sin(math.radians(alpha)) * x_scale
y_skew = x_skew#math.cos(math.radians(alpha)) * y_scale

alpha += 306.79876698156386
d=(width**2+height**2)**0.5
x_coor = coor[0]+d*math.sin(math.radians(alpha))
y_coor = coor[1]+d*math.cos(math.radians(alpha))

gt = [coor[0]-width/2, x_scale, x_skew, coor[1]-height/2, y_skew, y_scale]

# Set location
dst_ds.SetGeoTransform(gt)

# Get raster projection
epsg = 4326
srs = osr.SpatialReference()
srs.ImportFromEPSG(epsg)
dest_wkt = srs.ExportToWkt()

# Set projection
dst_ds.SetProjection(dest_wkt)

# Close files
dst_ds = None
src_ds = None