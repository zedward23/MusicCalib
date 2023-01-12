import Metashape
import os

###################################
# some hard-coded parameters
###################################
base_folder = '/media/chengp/RuggedLinux/MusicData/11_03'
instrument = 'piano'
save_folder = os.path.join(base_folder, instrument, 'agisoft_data_demo')

save_file = instrument + '.psx'

##################################
# export camera data
##################################
doc = Metashape.app.document
# doc.open(os.path.join(base_folder, save_file))
chunk = doc.chunk

chunk.exportCameras(os.path.join(save_folder, 'camera_pose.xml'))
# export to txt
cam_pose_filename = os.path.join(save_folder, 'cam_pose.txt')
file = open(cam_pose_filename, "wt")
for camera in chunk.cameras:
    if not camera.transform:
        continue
    Twc = camera.transform
    calib = camera.sensor.calibration
    file.write(
        "{:6d}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t\n".format(
            camera.key, Twc[0, 0], Twc[1, 0], Twc[2, 0], Twc[0, 1], Twc[1, 1], Twc[2, 1], Twc[0, 2], Twc[1, 2],
            Twc[2, 2], Twc[0, 3], Twc[1, 3], Twc[2, 3]))
file.flush()
file.close()
# export image name
im_name_filename = os.path.join(save_folder, 'im_name.txt')
file = open(im_name_filename, "wt")
for camera in chunk.cameras:
    if not camera.transform:
        continue
    path = camera.photo.path
    file.write("{:6d}\t{:s}\n".format(camera.key, path))
file.flush()
file.close()
