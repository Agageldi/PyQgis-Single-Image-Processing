from osgeo import gdal, osr
import math


src_filename ='/home/user/thesis/IMG_0048_4.tif'
dst_filename = '/home/user/thesis/output.tif'

def myImageGeoReference(src_filename,dst_filename):
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
    myEXIF = main_dic[src_filename]
    coor = myEXIF["gps"]

    groundheight = 238

    Radius = 6371000.
    flightHeight = coor[2]-groundheight

    dx=89.04573706*flightHeight/100
    dy=66.9190639*flightHeight/100

    rx=myEXIF["size"][0]
    ry=myEXIF["size"][1]

    width  = dx  #(  Radius*math.cos( math.radians(coor[1]) )  ))
    height = -dy

    x_scale = width/rx
    y_scale = height/ry

    alpha = myEXIF["azimuth"]
    x_skew = -math.sin(math.radians(alpha)) * x_scale
    y_skew = math.sin(math.radians(alpha))  * y_scale#math.cos(math.radians(alpha)) * y_scale

    x_scale = math.cos(math.radians(alpha)) * x_scale
    y_scale = math.cos(math.radians(alpha)) * y_scale

    alpha = alpha + 306.79876698156386
    d=(width**2+height**2)**0.5
    x_coor = coor[0]+d/2*math.sin(math.radians(alpha))-20
    y_coor = coor[1]+d/2*math.cos(math.radians(alpha))-11.2

    #x_coor = coor[0]-width/2
    #y_coor = coor[1]-height/2

    gt = [x_coor, x_scale, x_skew, y_coor, y_skew, y_scale]

    # Set location
    dst_ds.SetGeoTransform(gt)

    # Get raster projection
    epsg = 3857
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(epsg)
    dest_wkt = srs.ExportToWkt()

    # Set projection
    dst_ds.SetProjection(dest_wkt)

    # Close files
    dst_ds = None
    src_ds = None