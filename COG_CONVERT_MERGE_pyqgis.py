from osgeo import gdal

gdal.UseExceptions()

parent = iface.mainWindow()

inp,inpOk=QFileDialog.getOpenFileNames(parent,"Files to open", QgsProject.instance().homePath(),"GeoTIFF(*.Tif)")

driver = gdal.GetDriverByName("COG")
driver.Register()
translate_options = gdal.TranslateOptions(gdal.ParseCommandLine("-of COG -co COMPRESS=JPEG -co PHOTOMETRIC=YCBCR"))
fns=[]

for in_path in inp:
      src_ds = gdal.Open((in_path))
      out_path=in_path+"._COG.tif"
      gdal.Translate(out_path,src_ds,options=translate_options)
      fns.append(out_path)
      print("Succesfully Converted {}...".format(in_path))

QMessageBox.information(parent, "Success", "Succesfully Converted {}...".format(inp))
print("Success!")   

gdal.BuildVRT('vrt.vrt',fns)
gdal.Translate(inp[0]+"_mozaic.tif",'vrt.vrt',options=translate_options)


QMessageBox.information(parent, "Success", "Succesfully Converted and Merged")
print("Success!")   