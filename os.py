import os, qgis.core
from qgis.PyQt.QtCore import QVariant

path = "/home/user/temp_shared/Tag04_Flug03/MS"
#path = "/media/sf_shared/001/output3"
#get all files from directory
    #azimuth function
def myAzimuth(a,b):
    p1 = QgsPoint(a[0],a[1])
    p2 = QgsPoint(b[0],b[1])
    a = p1.azimuth(p2)
    if a < 0:
        a += 360
    return a


Qpoints=[]
Attributes=[]

main_dic = {}
points=[]
file_list=[]

def osLoop(path):
    print path
    file_list0 = os.listdir(path)
    file_list0.sort()


    
    for i in range(len(file_list0)):
        #folder recursively processing
        if os.path.splitext(file_list0[i])[1] == "":
            osLoop(path+"/"+file_list0[i])
            continue
        #skip other files 
        if file_list0[i][-5:].upper() !='1.TIF':
            continue
        file_list.append(path+"/"+file_list0[i])
#    print file_list

    """
    for i in range(len(file_list)):
        #skip folders and other files 
        if os.path.splitext(file_list[i])[1].upper() !='.TIF':
            continue
        #mergeBands(path+"/"+file_list[i][:-6])
    """
    #looping through the files
    for i in range(len(file_list)):
        #extracting all meta/exif data
        main_dic[file_list[i]]=myEXIFdata(file_list[i])
        main_dic[file_list[i]]['index'] = i
        main_dic[file_list[i]]['id']=os.path.basename(file_list[i])[4:8]
        
        
        points.append(main_dic[file_list[i]]["gps"])
        #creating Qgis point list
        Qpoints.append(QgsPoint(main_dic[file_list[i]]["gps"][0],main_dic[file_list[i]]["gps"][1]))
        Attributes.append(main_dic[file_list[i]])


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
            
        output = os.path.dirname(main_keys[i]) + "/output3/"+ os.path.basename(main_keys[i])
        #myImageGeoReference(main_keys[i],output)
    
def draw():
    #drawing points on the canvas
    shpName = "2_Tag4_Flug3"
    shpPath = "/media/sf_shared/2_shp/"+shpName+".shp"
    pointa = iface.addVectorLayer("Point?crs=epsg:3857&field=id:integer&index=yes",shpName,"memory")
    pointa.dataProvider().addAttributes([QgsField("id", QVariant.Int),QgsField("z", QVariant.Double),QgsField("azimuth", QVariant.Double),QgsField("time", QVariant.String),QgsField("Flug", QVariant.String),QgsField("Ort", QVariant.String),QgsField("Hohe", QVariant.Double),QgsField("Speed", QVariant.Double),QgsField("Wetter", QVariant.String),QgsField("LichtSensor", QVariant.String)])
    pointa.updateFields()
    
    myFlug = shpName
    myOrt = "camp-2"
    myHohe = 0
    mySpeed = 0
    myWetter = ''
    myLichtSensor = ''
    
    pointa.startEditing()
    feature = QgsFeature()
    medianHeight=Attributes[len(Attributes)/2]['gps'][2]
    Pnum = len(Qpoints)
    for p in Qpoints:
        index = Qpoints.index(p)
        #if Attributes[index]['gps'][2] < medianHeight - 5 and Attributes[index]['id'] < 100 or Attributes[index]['id']> Pnum-100:
        #    continue
        feature.setGeometry(QgsGeometry.fromPoint(p))
        feature.setAttributes([Attributes[index]['id'],Attributes[index]['gps'][2],Attributes[index]['azimuth'],Attributes[index]['timestamp'].isoformat(),myFlug,myOrt,myHohe,mySpeed,myWetter,myLichtSensor])
        pointa.addFeature(feature,True)
    pointa.commitChanges()
    iface.zoomToActiveLayer()
    
    QgsVectorFileWriter.writeAsVectorFormat(pointa,shpPath,"utf-8",None,"ESRI Shapefile")
    
    """
    #drawing line on the document
    linea = iface.addVectorLayer("LineString?crs=epsg:3857&field=id:integer&index=yes","Linea","memory")
    linea.startEditing()
    feature = QgsFeature()
    feature.setGeometry(QgsGeometry.fromPolyline(Qpoints))
    feature.setAttributes([1])
    linea.addFeature(feature,True)
    linea.commitChanges()
    iface.zoomToActiveLayer()
    """
    

osLoop(path)
draw()