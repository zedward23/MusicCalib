# MusicCalib

## build_3D_world_calibrate_gps.py
Reconstruct 3D world from the room scan. Build dense point cloud/mesh model for visual check. 
Register static gopros and aria. (Maybe let's move this part to a seperate function/file.)

## Register_fp_gopro.py
Register ego gopro camera frames. Registering too many frames simultaneously may result in computation cost. 
I usually do 300 images as a batch. Let's try to do it iteratively to cover all frames. 

## export_data.py
Export camera location and orientation. 

## aria_rgb.xml
aria intrinsics parameters. 

## static_gp.xml
gopro intrinsics parameters. 

## Extract gopro videos 
Use ffmpeg to extract videos into images. I use the resolution of 1920x1080 for gopro (half of the original resolution) to speed up the calculation. The gopro intrinsics parameters given are consistent with this resolution. 
For room scan use fps=5.

For static camera reconstruction, take a 1 minute clip of the video of playing and use fps=1 (60 images for each exo camera).

For ego cameras, use fps=30.

## Extract Aria videos 
Extracting images from Aria glass is a bit messy. We need to use Aria's codebase which is recommended to run in a container. 

To install the tools, refer to https://facebookresearch.github.io/Aria_data_tools/docs/Install/

To access the data, refer to https://facebookresearch.github.io/Aria_data_tools/docs/howto/dataprovider/

I used ./build/data_provider/examples/read_all <vrs_path> to read all the data out, which a little bit too much (preferably read only RGB images).

## Data for pipeline testing
https://drive.google.com/drive/folders/1RB-qnBBPgKp_h1hUWzKqx_9zi0winytx?usp=sharing
