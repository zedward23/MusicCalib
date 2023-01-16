import ffmpeg as fmpg
import sys
import subprocess
import os

#session = 'DryRun'
#instrument = 'Piano'
#camera = 'gp4'
#subject = 'Edward'
#videoPath = 'Cam04.mp4'
#fps = '1/60'

argumentList = sys.argv[1:]

#if (len(argumentList) != 7):
#    print("Wrong number of arguments")
#    exit()

session = argumentList[0]
instrument = argumentList[1]
camera = argumentList[2]
subject = argumentList[3]
videoPath = argumentList[4]
fps = argumentList[5]
dir = argumentList[6]

inputPath = os.path.join(dir, session + '\\' + instrument + '\\' + camera + '\\' + subject + '\\')
outputPath = os.path.join(dir, session + '\\' + instrument + '\\' + camera + '\\' + subject + '\\' + 'imgs\\')

os.chdir(dir)

subprocess.call(['ffmpeg', '-i', inputPath+videoPath, '-vf', 'fps='+fps, outputPath+'img%03d.png'])



print("hello world")