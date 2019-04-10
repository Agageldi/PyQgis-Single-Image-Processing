import os, qgis.core

path = "/media/sf_shared/001"

#get all files from directory
file_list = os.listdir(path)
file_list.sort()

main_dic = {}
points=[]
Qpoints=[]


#looping through the files
for i in range(len(file_list)):
    #skip folders and other files 
    if os.path.splitext(file_list[i])[1].upper() !='.TIF':
        continue
    #extracting all meta/exif data
    file_list[i] =path+"/"+file_list[i]
    main_dic[file_list[i]]=myEXIFdata(file_list[i])
    main_dic[file_list[i]]['index'] = i/6
    if i%6==0:
        points.append(main_dic[file_list[i]]["gps"])
        #creating Qgis point list
        Qpoints.append(QgsPoint(main_dic[file_list[i]]["gps"][0],main_dic[file_list[i]]["gps"][1]))

#azimuth function
def myAzimuth(a,b):
    p1 = QgsPoint(a[0],a[1])
    p2 = QgsPoint(b[0],b[1])
    a = p1.azimuth(p2)
    if a < 0:
        a += 360
    return a

#calculating azimuth attribute
PNum = len(points)
main_keys = main_dic.keys()
for i in range(len(main_dic)):
    x = main_dic[main_keys[i]]["index"]
    if x ==0:
        main_dic[main_keys[i]]["azimuth"] = myAzimuth(points[0],points[1])
    elif x == PNum-1:
        main_dic[main_keys[i]]["azimuth"] = myAzimuth(points[PNum-2],points[PNum-1])
    else:
        main_dic[main_keys[i]]["azimuth"] = myAzimuth(points[x-1],points[x])/2.+myAzimuth(points[x],points[x+1])/2.    
        
    output = os.path.dirname(main_keys[i]) + "/output/"+ os.path.basename(main_keys[i])
    myImageGeoReference(main_keys[i],output)
    

#drawing line on the document
"""
linea = iface.addVectorLayer("LineString?crs=epsg:4326&field=id:integer&index=yes","Linea","memory")
linea.startEditing()
feature = QgsFeature()
feature.setGeometry(QgsGeometry.fromPolyline(Qpoints))
feature.setAttributes([1])
linea.addFeature(feature,True)
linea.commitChanges()
iface.zoomToActiveLayer()
"""

#drawing points on the canvas
"""
pointa = iface.addVectorLayer("Point?crs=epsg:4326&field=id:integer&index=yes","Pointa","memory")
pointa.startEditing()
feature = QgsFeature()
i=0
for p in Qpoints:
    feature.setGeometry(QgsGeometry.fromPoint(p))
    feature.setAttributes([++i])
    pointa.addFeature(feature,True)
pointa.commitChanges()
iface.zoomToActiveLayer()
"""