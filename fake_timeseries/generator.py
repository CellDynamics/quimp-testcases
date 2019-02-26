# %%
import numpy as np
import matplotlib.pyplot as plt
from skimage.external.tifffile import imsave
from scipy.signal import gaussian
import math
X = 512
Y = 512


def circle(x0, y0, im, r):
    """
    Generate circle in image.

    x0, y0: center of the object
    im: image to generate object into
    r: radius

    Return:
    image with object
    """
    im = np.zeros(im.shape, dtype=im.dtype)
    x, y = np.meshgrid(range(0, im.shape[0]), range(0, im.shape[1]))
    im[(x-x0)**2+(y-y0)**2 < r*r] = 1
    return im


def timeline(t, im):
    """
    Generate linear movement.

    Return x,y coordinates for normalised time.

    t: vector of values in range <-1;1>. Each value is a timepoint

    Return
    (x,y) coordinates
    """
    start = im.shape[1]*0.1  # start point
    stop = im.shape[1] - start
    ts = (t-(np.min(t)))/np.ptp(t)  # assume range -1,1
    x = start+ts*(stop-start)
    y = np.array([256]*len(x))
    return x, y


def timegauss(t, im):
    """
    Generate Gaussian movement.

    Return x,y coordinates for normalised time.

    t: vector of values in range <-1;1>. Each value is a timepoint

    Return
    (x,y) coordinates for each timepoint
    """
    def gaussian(x, mu, sig):
        return 1./(np.sqrt(2.*np.pi)*sig)*np.exp(-np.power((x - mu)/sig, 2.)/2)
    start = im.shape[1]*0.1  # start point
    stop = im.shape[1] - start
    ts = (t-(np.min(t)))/np.ptp(t)  # assume range -1,1
    x = start+ts*(stop-start)
    g = gaussian(x, np.median(x), 50)
    g /= np.max(g)
    y = im.shape[0]*0.25 + g*im.shape[0]*0.5
    return x, y


def timeuturn(t, im):
    """
    Generate u-turn movement.

    Return x,y coordinates for normalised time.

    t: vector of values in range <-1;1>. Each value is a timepoint

    Return
    (x,y) coordinates for each timepoint
    """
    start = im.shape[1]*0.1  # start point
    stop = im.shape[1] - start  # end point
    # normalise time
    ts = (t-(np.min(t)))/np.ptp(t)  # assume range -1,1
    x = np.zeros(len(ts))
    y = np.zeros(len(ts))
    x_range_1 = ts <= 0.3
    x_range_2 = np.logical_and(ts > 0.3, ts <= 0.6)
    x_range_3 = ts > 0.6

    x[x_range_1] = start
    y[x_range_1] = np.linspace(im.shape[0]*0.25, im.shape[0]*0.75, np.sum(x_range_1))

    x[x_range_2] = np.linspace(im.shape[1]*0.25, im.shape[1]*0.75, np.sum(x_range_2))
    y[x_range_2] = im.shape[0]*0.75

    x[x_range_3] = stop
    y[x_range_3] = np.linspace(im.shape[0]*0.75, im.shape[0]*0.25, np.sum(x_range_3))
    return x, y


def generator(xres, yres, tres, shape_fcn, time_fcn, name, fg=255):
    """
    """
    im = np.zeros((X, Y))
    x, y = time_fcn(np.linspace(-1, 1, tres), im)
    stack = np.zeros((len(x), xres, yres), dtype=np.uint8)
    for i in range(stack.shape[0]):
        s = shape_fcn(x[i], y[i], stack[i])
        stack[i][s > 0] = fg
    imsave(name, stack)


generator(X, Y, 100,
          lambda x0, y0, im: circle(x0, y0, im, 25),
          timeline,
          "test.tif")

generator(X, Y, 100,
          lambda x0, y0, im: circle(x0, y0, im, 25),
          timegauss,
          "test2.tif")

generator(X, Y, 100,
          lambda x0, y0, im: circle(x0, y0, im, 25),
          timeuturn,
          "test3.tif")
