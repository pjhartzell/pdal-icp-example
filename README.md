# Moving Window ICP Example using PDAL
Reference implementation of [PDAL](https://pdal.io/) to estimate horizontal deformation caused by the August 2014 M6.0 earthquake that occurred in Napa, California.

## Lidar point cloud preparation
Three PDAL pipelines were applied to the pre- and post-event point clouds to extract ground and building (planar) points:
1. *ground_filter.json* - Identifies ground points and save them to a new LAZ file.
2. *plane_filter.json* - Identifies planar points and saves them to a new LAZ file.
3. *merge.json* - Crops and merges the two LAZ files created by the ground and plane filtering pipelines and saves the merged point cloud to a new LAZ file.

The pipelines are executed with PDAL's command line application in a terminal. For example, the following command will run the *ground_filter.json* pipeline:  
`$ pdal pipeline ground_filter.json`.

## Deformation estimation with PDAL's Iterative Closest Point (ICP) algorithm
PDAL's Python extension was used to apply ICP to moving windows of the prepared pre- and post-event point cloud data within a simple Python script. The window is moved (stepped) in the X and Y directions to produce multiple ICP solutions to estimate the spatially variable deformation. Within the script, a pipeline is generated and executed for each window location to extract (using [Entwine](https://entwine.io/) point indices) the pre- and post-event lidar data falling within the window, apply the ICP algorithm, and store the solved horizontal motion for eventual plotting. 

## Sample result
ICP solutions were generated with a 200 meter window and 100 meter step size and are shown in the image below. Note that differences with the published image are a result of uncorrected datum errors that exist in the raw lidar point clouds. These datum errors were estimated and removed in the published image by removing the mean motion on the west side of the fault from all vectors. See [Brocher et al. (2015)](https://doi.org/10.1785/0220150004) for details on the Napa earthquake. Spurious vector solutions in the southeast corner caused by a gap in point cloud data were also removed in the published image.  
![sample icp results](img/icp_vectors.png)
