import json
import matplotlib.pyplot as plt
import pdal


# ICP window and step sizes
window_size = 200
step_size = 100

# Path to pre- and post-event indexed point clouds (EPT)
pre_event_index = './data/ept/new/bv_06/ept.json'
post_event_index = './data/ept/new/bv_09/ept.json'

# Variables to hold the ICP vector origins (X, Y) and displacements (dx, dy)
X = []
Y = []
dx = []
dy = []

# Slide a window through the analysis area
for x in range(556627, 558726, step_size):
    for y in range(4238930, 4240977, step_size):

        # PDAL pipeline with data bounds set according to the current window.
        # The first window is 'fixed'; The second window is 'moving'.
        # Note that we pad the 'fixed' window so the second window has room to
        # move within the fixed window as the ICP solution converges.
        pipeline = [
            {
                'type':'readers.ept',
                'filename':post_event_index,
                'bounds':'([{},{}],[{},{}])'.format(x - 2,
                                                    x + window_size + 2,
                                                    y - 2,
                                                    y + window_size + 2)
            },
            {
                'type':'readers.ept',
                'filename':pre_event_index,
                'bounds':'([{},{}],[{},{}])'.format(x,
                                                    x + window_size,
                                                    y,
                                                    y + window_size)
            },
            {
                'type':'filters.icp'
            }
        ]

        # Execute the pipeline
        p = pdal.Pipeline(json.dumps(pipeline))
        p.validate()
        p.execute()

        # Capture the metadata, which contains the ICP transformation
        m = json.loads(p.metadata)
        t = m.get('metadata').get('filters.icp')[0].get('transform')

        # Store vector origin and ICP-derived displacement
        try:
            t = [float(val) for val in t.split()]
            X.append(x + window_size/2)
            Y.append(y + window_size/2)
            dx.append(t[3])
            dy.append(t[7])
        except:
            pass

        # Print status
        print('Displacement vector at X={}, Y={}: dx={}, dy={}'.format(
            X[-1], Y[-1], dx[-1], dy[-1]))

# Plot the ICP vectors
plt.figure()
plt.quiver(X, Y, dx, dy, angles='xy', scale_units='xy')
plt.axis('equal')
plt.show()
