# DeadPixelAveragingAlgorithm
Used to eliminate dead pixels from images from the camera

1) ChecLabPy in folder ../Folder_name/CHECLabPy
2) Download files and place in ../Folder_name/DeadPixelAlgorithm
3) In DeadPixelAveragingAlgorithm.py, define whether the files that are to be read in are a single module or the full camera
4) In DPAABE.py, define which file is being read in

At the moment, the script randomly selects which pixel is dead. Eventually a pandas dataframe set could be used to identify which pixels are dead.
