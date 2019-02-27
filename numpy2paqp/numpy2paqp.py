"""Conversion tool numpy<->paqp."""

import argparse
import numpy as np
import os
import logging
from datetime import datetime
import random
from skimage.external.tifffile import imsave

logger = logging.getLogger(__name__)
if logger.hasHandlers():
    logger.handlers.clear()
ch = logging.StreamHandler()
logger.addHandler(ch)
logger.setLevel("DEBUG")

parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input file. Extension determines conversion direction")
parser.add_argument("output", help="Destination file")
parser.add_argument("--image", help="Image related to this dataset. If not specified, empty image will be generated")
args = parser.parse_args()


def getImage(path, slices, res=(512, 512)):
    """
    Generate fake tiff.

    Args:
    path (str):     nam and path of the image
    slices (int):   number of slices
    res (int,int):  resolution
    """
    image = np.zeros((slices, *res), dtype=np.uint8)
    imsave(path, image)
    logger.debug('Created image {}'.format(path))


def getSnName(rootname):
    """
    Create Snake file name from specified name.

    Args:
    rootname (path):    root name, can have extension

    Returns:
    rootname.snQP
    """
    relname = os.path.basename(rootname)
    relname = os.path.join('.', relname)
    if not os.path.splitext(relname)[1]:
        return relname+'_0.snQP'
    else:
        return os.path.splitext(relname)[0]+'_0.snQP'


def generatepaQP(name, frames):
    """
    Recreate paQP file.

    Args:
        name (path):    name and path of the output file.
        frames (int):   number of frames
     """
    snakefile = getSnName(name)
    logger.debug("Snake file name {}".format(snakefile))
    if not os.path.splitext(name)[1]:
        name += '_0.paQP'
    else:
        name = os.path.splitext(name)[0]+'_0.paQP'
    logger.debug(f"Writing paQP at: {name}")
    with open(name, 'w') as stream:
        stream.write("#p2 - QuimP parameter file (QuimP11). Created {}\n".format(datetime.now()))
        stream.write(str(random.randint(0, 10000))+'\n')
        stream.write(args.image+'\n')
        stream.write(snakefile+'\n')
        stream.write("#Image calibration (scale, frame interval)\n")
        stream.write("1.00\n")
        stream.write("1.00\n")
        stream.write("#segmentation parameters (Maximum number of nodes, ND, Max iterations, Node spacing, Blowup, Sample tan, Sample norm, Crit velocity, Central F, Contract F, ND, Image force, ND)\n")
        stream.write("250\n")
        stream.write("1.0\n")
        stream.write("4000.0\n")
        stream.write("4.2\n")
        stream.write("20.0\n")
        stream.write("4\n")
        stream.write("12\n")
        stream.write("0.005\n")
        stream.write("0.04\n")
        stream.write("0.04\n")
        stream.write("0.6\n")
        stream.write("0.2\n")
        stream.write("0.5\n")
        stream.write("# - new parameters (cortex width, start frame, end frame, final shrink, statsQP, fluImage)\n")
        stream.write("1.0\n")
        stream.write("1\n")
        stream.write("{:d}\n".format(frames))
        stream.write("4.0\n")
        stream.write("none.csv\n")
        stream.write("# - Fluorescence channel tiff's\n")
        stream.write("./\n")
        stream.write("./\n")
        stream.write("./\n")
        stream.write("#END")


def getDistances(xy):
    """
    Compute distances between pixels in contour.

    Args:
    xy (numpy): 2 column array (x,y) of pixels

    Return
    dist (numpy):   An array of size array.shape - 1 of distances between pixels
    """
    xys = np.roll(xy, -1, 0)  # shifted upwards
    dist = np.sqrt(np.sum((xy-xys)**2, axis=1))
    return dist  # FIXME: delete last element which is distance between last and first point (after np.roll)


def rescale(array, res=(512, 512)):
    coords = array[:, 1:]  # get rid of frame number
    sh = coords.shape
    xy = coords.reshape((-1, 2))  # 2 columns
    xy = xy - np.mean(xy, axis=0)  # center
    xy = xy + np.array([res[0]/2, res[1]/2])
    array[:, 1:] = xy.reshape(sh)
    return array


def saveFrames(array, stream, res=(512, 512)):
    """
    Save frames from numpy data file.
    """
    for f in array:
        frame = f[0]
        coords = f[1:]
        xy = coords.reshape((-1, 2))
        dist = getDistances(xy)
        lenght = np.sum(dist)
        stream.write("#Frame {:.0f}\n".format(frame))
        stream.write("{:.0f}\n".format(coords.shape[0]//2))
        d = 0.
        for i, (p, ptp) in enumerate(zip(xy, dist)):  # over points,distances between them
            pos = d / lenght
            d += ptp
            stream.write(
                "{position:.6f}\t{xcoord:.2f}\t{ycoord:.2f}\t{position:.6f}\t{position:.6f}\t{speed:.6f}\t{flu:.2f}\t{c:.6f}\t{c:.6f}\t{flu:.2f}\t{c:.6f}\t{c:.6f}\t{flu:.2f}\t{c:.6f}\t{c:.6f}\n"
                .format(position=pos,
                        xcoord=p[0],
                        ycoord=p[1],
                        speed=0.0,
                        flu=0.0,
                        c=-2.))


def generatesnQp(name):
    """Write snake file."""
    snakefile = getSnName(name)
    snakefile_abs = os.path.join(os.path.dirname(name), os.path.basename(snakefile))
    array = rescale(np.loadtxt(args.input))
    logger.debug(f"Writing snQP at: {snakefile_abs}")
    with open(snakefile_abs, 'w') as stream:
        stream.write("#QuimP11 node data\n")
        stream.write(
            "#Node Position	X-coord	Y-coord	Origin	G-Origin	Speed	Fluor_Ch1	Ch1_x	Ch1_y	Fluor_Ch2	Ch2_x	Ch2_y	Fluor_CH3	CH3_x	Ch3_y\n")
        stream.write("#\n")
        saveFrames(array, stream)


if "txt" in os.path.splitext(args.input)[1]:
    logger.debug("Converting txt->paQp")
    frames = np.loadtxt(args.input).shape[0]
    if args.image is None:
        args.image = os.path.abspath(os.path.join(os.path.dirname(args.output), 'image.tif'))
        getImage(args.image, frames)

    generatepaQP(args.output, frames)
    generatesnQp(args.output)
