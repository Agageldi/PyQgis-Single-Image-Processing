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
    #extracting all meta/exif data
    main_dic[file_list[i]]=myEXIFdata(path+"/"+file_list[i])
    if i%6==0:
        points.append(main_dic[file_list[i]]["gps"])
        #creating Qgis point list
        Qpoints.append(QgsPoint(main_dic[file_list[i]]["gps"][0],main_dic[file_list[i]]["gps"][1]))

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