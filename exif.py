#sudo pip install ExifRead
import exifread

def myEXIFdata(src_filename):
    # Open image file for reading (binary mode)
    f = open(src_filename, 'rb')

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
            
        return coor
        
    #keys = tags.keys()
    gpsKeys = ['GPS GPSLongitude','GPS GPSLatitude','GPS GPSAltitude']
    return getValueOfTag(gpsKeys)