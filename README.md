# MusicCalib

build_3D_world_calibrate_gps.py:
Reconstruct 3D world from the room scan. Build dense point cloud/mesh model for visual check. 
Register static gopros and aria. (Maybe let's move this part to a seperate function/file.)

Register_fp_gopro.py:
Register ego gopro camera frames. Registering too many frames simultaneously may result in computation cost. 
I usually do 300 images as a batch. Let's try to do it iteratively to cover all frames. 

export_data.py:
Export camera location and orientation. 

aria_rgb.xml: aria intrinsics parameters. 
static_gp.xml: gopro intrinsics parameters. 

