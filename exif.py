#sudo pip install ExifRead
import exifread
from datetime import datetime
from pyproj import Proj

#projection WGS84/Pseudo Mecarto
proj_4326 = Proj(init="epsg:3857", preserve_units=False)




def myEXIFdata(src_filename):
    # Open image file for reading (binary mode)
    f = open(src_filename, 'rb')
    exif={}

    # Return Exif tags
    tags = exifread.process_file(f)

    #converting instance to double
    def getValueOfTag(gpsKeys):
        coor = []
        for i in range(3):
            v=tags[gpsKeys[i]].values
            if len(v) >1:
                c=v[0].num+v[1].num/60.+v[2].num*1./v[2].den/3600.
            else:
                c=v[0].num*1./v[0].den
            coor.append(c)
            
        coor[0], coor[1] = proj_4326(coor[0],coor[1])
        return coor
        
    #keys = tags.keys()
    gpsKeys = ['GPS GPSLongitude','GPS GPSLatitude','GPS GPSAltitude']
    exif["gps"] = getValueOfTag(gpsKeys)
    
    v=tags["Image DateTime"].values
    exif["timestamp"]=datetime.strptime(v,"%Y:%m:%d %H:%M:%S")
    
    exif["size"] = [tags['Image ImageWidth'].values[0],tags['Image ImageLength'].values[0]]
    
    f.close()
    return exif