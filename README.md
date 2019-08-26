# pdal-icp-example
Reference implementation of [PDAL](https://pdal.io/) to estimate deformation caused by an earthquake.

### Lidar point cloud preparation
Three PDAL pipelines (a series of PDAL stages) are applied to the pre- and post-event point clouds to extract ground and building (planar) points:
1. ground_filter.json - Identifies ground points and stores them in a new LAZ file.
2. plane_filter.json - Identifies planar points and stores them in a new LAZ file.
3. merge.json - Merges the two LAZ files created by the ground and plane filtering pipelines and stores the data in a new LAZ file.

The pipelines are executed with PDAL's pipeline *application* in a terminal, e.g., `pdal pipeline ground_filter.json`.

### Deformation estimation with PDAL's Iterative Closest Point (ICP) algorithm
PDAL's Python extension is used to apply ICP to windows of the prepared pre- and post-event point cloud data within a simple Python script. The window is moved (stepped) in the X and Y directions to produce multiple ICP solutions to estimate the spatially variable deformation. Within the script, a pipeline is generated and executed for each window location to extract (using [Entwine](https://entwine.io/) point indices) the pre- and post-event lidar data falling within the window, apply the ICP algorithm, and store the solved horizontal motion for eventual plotting. 

### Sample result
Generated with a 200m window and 100m step size. Note: the discrepancy with the published image is due to uncorrected datum errors in the raw lidar point clouds.
![sample icp results](sample_icp_200w_100s.png)
