from osgeo import gdal
import time
import processing
import csv

start_time = time.time()

gdal.UseExceptions()

parent = iface.mainWindow()

inp,inpOk=QFileDialog.getOpenFileNames(parent,"Files to open", QgsProject.instance().homePath(),"GeoTIFF(*.Tif)")
outp,outpOK=QFileDialog.getSaveFileName(parent,"Converted and Merged Files Directory", QgsProject.instance().homePath(),"GeoTIFF(*.Tif)")
clis, cliOK = QFileDialog.getOpenFileName(parent,"Shapefiles to be mask", QgsProject.instance().homePath(),"Shape Files (*.shp);;GeoJSON Files (*.geojson)")
clos, cloOK = QFileDialog.getSaveFileName(parent,"Clip Files Directory", QgsProject.instance().homePath(),"GeoTIFF(*.Tif)")
fcsv,fcsvOk=QFileDialog.getOpenFileName(parent,"Table to clip", QgsProject.instance().homePath(),"Comma Delimited Text(*.csv)")

driver = gdal.GetDriverByName("COG")
driver.Register()
translate_options = gdal.TranslateOptions(gdal.ParseCommandLine("-of COG -co COMPRESS=JPEG -co PHOTOMETRIC=YCBCR"))
fns=[]
i=0

for in_path in inp:
      src_ds = gdal.Open((in_path))
      out_path=outp.replace(".Tif","_"+str(i)+".Tif")
      gdal.Translate(out_path,src_ds,options=translate_options)
      fns.append(out_path)
      i+=1
      print("Succesfully Converted {}...".format(in_path))

mo_out=outp.replace(".Tif","_"+"mozaic"+".Tif")
vrt=outp.replace(".Tif",".vrt")
gdal.BuildVRT(vrt,fns)
gdal.Translate(mo_out,vrt,options=translate_options)

tifin=QgsRasterLayer(mo_out,"Raster Later", "gdal")
shpin=QgsVectorLayer(clis,"Vector Layer", "ogr")

lol=[]

with open(fcsv, 'r') as read_obj: # read csv file as a list of lists
     csv_reader= csv.reader(read_obj, delimiter=';')# pass the file object to reader() to get the reader object
     next(csv_reader)
     
     for row in csv_reader:
        lol.append(row)

j=0

for l in lol:
     comp=l[1]
     outRaster = clos.replace(".Tif","_"+comp+".Tif")
     clipv=clis.replace(".shp","_"+'{}'+".shp").format(comp)
     q="COMPID ='{}'".format(comp)
     shpin.selectByExpression(q)
     QgsVectorFileWriter.writeAsVectorFormat(shpin,clipv, "utf-8",shpin.crs(), "ESRI Shapefile", onlySelected=True)
     processing.run("gdal:cliprasterbymasklayer",
     {'INPUT':tifin, 'MASK':clipv, 'ALPHA_BAND':True, 'OUTPUT':outRaster})

seconds = time.time() - start_time
print('Time Taken:', time.strftime("%H:%M:%S",time.gmtime(seconds)))

QMessageBox.information(parent, "Success", "Succesfully Processed!!!")
print("Success!")   