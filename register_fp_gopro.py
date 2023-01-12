import Metashape
import os

agisoft_LICENSE = "/home/chengp/Documents/metashape-pro/metashape.lic"

###################################
# some hard-coded parameters
###################################
base_folder = '/media/chengp/RuggedLinux/MusicData/11_03'
fp_gp_folder = os.path.join(base_folder, 'piano/head_gp/images')

calib_file = os.path.join(base_folder, 'head_mounted_gp.xml')

save_file = 'piano_complete.psx'

###################################
# register head mounted gopro camera
###################################
doc = Metashape.app.document
doc.open(os.path.join(base_folder, save_file))
chunk = doc.chunk


#### head mounted gopro camera ####
# prepare file list
filelist = os.listdir(fp_gp_folder)
absolute_filelist = [os.path.join(fp_gp_folder, filepath) for filepath in filelist]
absolute_filelist.sort()
absolute_filelist = absolute_filelist[4500:4800]
absolute_filelist.sort()
# add photo
chunk.addPhotos(absolute_filelist)
# add camera and assign the photos to it
sensor = chunk.addSensor()
calibration = Metashape.Calibration()
calibration.load(calib_file)
sensor.label = 'head_mounted_gopro'
sensor.type = Metashape.Sensor.Type.Fisheye
sensor.width = calibration.width
sensor.height = calibration.height
sensor.user_calib = calibration.copy()
sensor.fixed = True
print(sensor.type)
for camera in chunk.cameras:
    if camera.label[:7] == 'head_gp':
        camera.sensor = sensor
# match points and align camera
chunk.matchPhotos(downscale=0, reference_preselection=False, keep_keypoints=True)
chunk.alignCameras(reset_alignment=False)
# save project
doc.save(os.path.join(base_folder, save_file))

exit()