# Moving Window ICP Example using PDAL
A reference implementation of [PDAL](https://pdal.io/) to estimate horizontal deformation caused by the August 2014 M6.0 earthquake that occurred in Napa, California.

## Lidar point cloud preparation
Three PDAL pipelines were applied to the pre- and post-event point clouds to extract ground and building (planar) points:
1. *ground_filter.json* - Identifies ground points and saves them to a new LAZ file.
2. *plane_filter.json* - Identifies planar points and saves them to a new LAZ file.
3. *merge.json* - Crops and merges the two LAZ files created by the ground and plane filtering pipelines and saves the merged data to a new LAZ file.

The pipelines are executed with PDAL's command line application in a terminal. For example, the following command will run the *ground_filter.json* pipeline:  
`$ pdal pipeline ground_filter.json`.

## Deformation estimation with PDAL's Iterative Closest Point (ICP) algorithm
PDAL's Python extension is used within a simple Python script to apply ICP to a small window of the prepared pre- and post-event point cloud data. By repetitively moving the window location in a systematic manner (regular steps in the X and Y directions), a gridded estimate of the spatially variable ground motion is created. Prior to executing the script, the prepared point cloud data is indexed into [Entwine](https://entwine.io/) point tiles (EPT) for efficient extraction of the window locations from the point cloud data.

## Sample result
ICP solutions were generated with a 200 meter window and 100 meter step size in this example. The horizontal components of the solutions are shown in the image below. Note that differences with the published image are a result of uncorrected datum errors that exist in the raw lidar point clouds. These datum errors were estimated and removed in the published image by removing the mean motion on the west side of the fault from all vectors. See [Brocher et al. (2015)](https://doi.org/10.1785/0220150004) for details on the Napa earthquake. Spurious vector solutions in the southeast corner caused by a gap in point cloud data were also removed in the published image.  
![sample icp results](img/icp_vectors.png)
