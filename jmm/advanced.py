#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

from PIL import Image


def ndarrayAsImage(a_np_ndarray, size=None, channels=3):
    """Turns a numpy ndarray into an image.
    :param a_np_ndarray: a numpy ndarray
    :param tuple size: the size of the picture in pixels. Use this option to parse the image differently.
                    But you would prefer resizing the input numpy array instead.
    :param int channels: the number of channels (3 for rgb for instance). Default: 3
    """
    # https://stackoverflow.com/questions/2659312/how-do-i-convert-a-numpy-array-to-and-display-an-image

    if size is None:
        assert len(a_np_ndarray.shape) in [2,3], "Does not support yet multiple images at a time within the same ndarray"
        if len(a_np_ndarray.shape) == 2:
            w, h = a_np_ndarray.shape[:2]
        elif len(a_np_ndarray.shape) == 3:
            w, h, channels = a_np_ndarray.shape[:3]
    else:
        w, h = size

    data = np.zeros((h, w, channels), dtype=np.uint8)
    # data[0:256, 0:256] = [255, 0, 0] # red patch in upper left if `w, h = (512, 512)`
    data[:w, :h] = a_np_ndarray
    img = Image.fromarray(data, 'RGB')
    return img


ndarray_as_image = ndarrayAsImage

