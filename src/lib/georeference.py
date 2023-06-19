'''
This module georeferences images based on
the calibrated theta and phis matrices
'''

import cv2
import numpy as np
from typing import Tuple

import config_vars

def distance_warp(image, thetas, phis) -> Tuple(np.ndarray, Tuple[int, int], int):
    '''
    These three arrays must all have the same shape.
    Each pixel 
    '''
    assert image.shape == thetas.shape
    assert image.shape == phis.shape
    x_coords = np.cos(thetas) * np.tan(phis) * (phis < config_vars.ANGLE_WARP_PHI_CUTOFF)
    y_coords = np.sin(thetas) * np.tan(phis) * (phis < config_vars.ANGLE_WARP_PHI_CUTOFF)
    # TODO: create an OpenCV mapping and interpolate by closest val
    # TODO: return a warped image, center pixels (drone pos), cm/px
    
