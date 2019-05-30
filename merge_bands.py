def mergeBands(inputString):
    inputfiles =  inputString+"_1.tif "
    inputfiles +=  inputString+"_2.tif " #"band3_clip.tif band4_clip.tif band5_clip.tif"
    inputfiles +=  inputString+"_3.tif "
    inputfiles +=  inputString+"_4.tif "
    inputfiles +=  inputString+"_5.tif "
    inputfiles +=  inputString+"_6.tif "
    outputfile =  os.path.dirname(inputString+"._1.tif")+"/merged/"+os.path.basename(inputString+".tif")

    # Generate the command
    command = "gdal_merge.py -separate %s -o %s" % (inputfiles, outputfile)
    command = "gdal_merge.py -separate -of HFA -o %s %s " % ( outputfile, inputfiles)
    #gdal_merge.py -separate -of HFA -o /media/sf_shared/001/output3/merged/IMG_0040.tif /media/sf_shared/001/output3/IMG_0040_1.tif /media/sf_shared/001/output3/IMG_0040_2.tif /media/sf_shared/001/output3/IMG_0040_3.tif /media/sf_shared/001/output3/IMG_0040_4.tif /media/sf_shared/001/output3/IMG_0040_5.tif /media/sf_shared/001/output3/IMG_0040_6.tif
    print command

    # Run the command. os.system() returns value zero if the command was executed succesfully
    os.system(command)