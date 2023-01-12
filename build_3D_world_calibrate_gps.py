import Metashape
import os

# agisoft_LICENSE = "/home/chengp/Documents/metashape-pro/metashape.lic"

###################################
# some hard-coded parameters
###################################
base_folder = '/media/chengp/RuggedLinux/MusicData/11_03'
instrument = 'piano'

env_im_folder = [os.path.join(base_folder, instrument, 'new_recon_images'), os.path.join(base_folder, instrument, 'recon_images')]
static_cam = ['cam02', 'cam03', 'cam04']
static_aria_folder = os.path.join(base_folder, instrument, 'aria02/data/214-1')

calib_file = os.path.join(base_folder, 'head_mounted_gp.xml')
static_calib_file = os.path.join(base_folder, 'static_gp.xml')
aria_calib_file = os.path.join(base_folder, 'aria_rgb.xml')

save_file = instrument + '_complete.psx'

##################################
# build 3D environment and register cameras
##################################
# doc = Metashape.Document()
# chunk = doc.addChunk()
# doc.save(os.path.join(base_folder, save_file))

doc = Metashape.app.document
chunk = doc.chunk

### build 3D environment by room scan ####
# prepare file list
absolute_filelist = []
for folder in env_im_folder:
    filelist = os.listdir(folder)
    ab_filelist = [os.path.join(folder, filepath) for filepath in filelist]
    absolute_filelist = absolute_filelist + ab_filelist
absolute_filelist.sort()
# add photo
chunk.addPhotos(absolute_filelist)
# add camera and assign the photos to it
sensor = chunk.addSensor()
calibration = Metashape.Calibration()
calibration.load(static_calib_file)
sensor.label = 'gopro_head_mounted'
sensor.type = Metashape.Sensor.Type.Fisheye
sensor.width = calibration.width
sensor.height = calibration.height
sensor.user_calib = calibration.copy()
print(sensor.type)
for camera in chunk.cameras:
    camera.sensor = sensor
# match points and align camera
chunk.matchPhotos(downscale=0, reference_preselection=False, keep_keypoints=True)
chunk.alignCameras(reset_alignment=False)
# save project
doc.save(os.path.join(base_folder, save_file))


### reconstruct dense cloud ####
# reload from saved project
doc = Metashape.app.document
doc.open(os.path.join(base_folder, save_file))
chunk = doc.chunk

# build depth maps and dense point cloud
chunk.buildDepthMaps(downscale=1)
chunk.buildDenseCloud() # optionally
# build mesh model
chunk.buildModel(surface_type=Metashape.Arbitrary, interpolation=Metashape.EnabledInterpolation,
                 source_data=Metashape.DepthMapsData)
doc.save(os.path.join(base_folder, save_file))


#### register static camera ####
doc = Metashape.app.document
doc.open(os.path.join(base_folder, save_file))
chunk = doc.chunk

for cam in static_cam:
    # prepare file list
    folder_path = os.path.join(base_folder, instrument, cam, 'recon_images')
    filelist = os.listdir(folder_path)
    absolute_filelist = [os.path.join(folder_path, filepath) for filepath in filelist]
    absolute_filelist.sort()
    # add photo
    chunk.addPhotos(absolute_filelist)
    # add camera and assign the photos to it
    sensor = chunk.addSensor()
    calibration = Metashape.Calibration()
    calibration.load(static_calib_file)
    sensor.label = cam
    sensor.type = Metashape.Sensor.Type.Fisheye
    sensor.width = calibration.width
    sensor.height = calibration.height
    sensor.user_calib = calibration.copy()
    sensor.fixed = True
    print(sensor.type)
    group = chunk.addCameraGroup()
    group.type = Metashape.CameraGroup.Station
    for camera in chunk.cameras:
        if camera.label[:5] == cam:
            camera.sensor = sensor
            camera.group = group
    # match points and align camera
    chunk.matchPhotos(downscale=0, reference_preselection=False, keep_keypoints=True)
    chunk.alignCameras(reset_alignment=False)

# save project
doc.save(os.path.join(base_folder, save_file))

#### register static aria ####
# prepare file list
filelist = os.listdir(static_aria_folder)
absolute_filelist = [os.path.join(static_aria_folder, filepath) for filepath in filelist]
absolute_filelist.sort()
absolute_filelist = absolute_filelist[1800:3600]
absolute_filelist = absolute_filelist[::30]
# add photo
chunk.addPhotos(absolute_filelist)
# add camera and assign the photos to it
sensor = chunk.addSensor()
calibration = Metashape.Calibration()
calibration.load(aria_calib_file)
sensor.label = 'static_aria'
sensor.type = Metashape.Sensor.Type.Fisheye
sensor.width = calibration.width
sensor.height = calibration.height
sensor.user_calib = calibration.copy()
sensor.fixed = True
print(sensor.type)
group = chunk.addCameraGroup()
group.type = Metashape.CameraGroup.Station
for camera in chunk.cameras:
    if camera.label[:5] == '214-1':
        camera.sensor = sensor
        camera.group = group
# match points and align camera
chunk.matchPhotos(downscale=0, reference_preselection=False, keep_keypoints=True)
chunk.alignCameras(reset_alignment=False)

# save project
doc.save(os.path.join(base_folder, save_file))
