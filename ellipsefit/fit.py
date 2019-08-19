#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
R. Patrick Xian adapted from
http://nicky.vanforeest.com/misc/fitEllipse/fitEllipse.html
"""

import numpy as np
from numpy.linalg import eig, inv
import matplotlib.pyplot as plt

def fitEllipse(x, y):
    """
    Ellipse fitting using the least squares method
    """

    x = x[:, None]
    y = y[:, None]
    D =  np.hstack((x*x, x*y, y*y, x, y, np.ones_like(x)))
    S = np.dot(D.T, D)

    C = np.zeros([6, 6])
    C[0, 2], C[2, 0] = 2, 2
    C[1, 1] = -1

    E, V = eig(np.dot(inv(S), C))
    n = np.argmax(np.abs(E))
    a = V[:, n]

    return a


def ellipse_center(a):
    """
    Retrieve the center of ellipse from fitting parameters
    """

    b, c, d, f, g, a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    num = b*b - a*c
    x0 = (c*d - b*f) / num
    y0 = (a*f - b*d) / num

    return np.array([x0, y0])


def ellipse_axis_length(a):
    """
    Retrieve the ellipse axis lengths from fitting parameters
    """

    b, c, d, f, g, a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    up = 2*(a*f*f + c*d*d + g*b*b - 2*b*d*f - a*c*g)

    down1 = (b*b-a*c) * ((c-a) * np.sqrt(1+4*b*b/((a-c)*(a-c))) - (c+a))
    down2 = (b*b-a*c) * ((a-c) * np.sqrt(1+4*b*b/((a-c)*(a-c))) - (c+a))

    res1 = np.sqrt(up/down1)
    res2 = np.sqrt(up/down2)

    return np.array([res1, res2])


def ellipse_angle_of_rotation(a):
    """
    Retrieve the angle of rotation from fitting parameters
    """

    b, c, d, f, g, a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]

    if b == 0:
        if a > c:
            return 0
        else:
            return np.pi/2

    else:
        if a > c:
            return np.arctan(2*b/(a-c))/2
        else:
            return np.pi/2 + np.arctan(2*b/(a-c))/2


def fitEllipseParams(*coords, plot=False, img=None, **kwds):
    """
    Direct least-squares method for fitting ellipse from scattered points
    """

    rcoords, ccoords = coords
    fitvec = fitEllipse(rcoords, ccoords)

    # Calculate the ellipse parameters
    center = ellipse_center(fitvec)
    phi = ellipse_angle_of_rotation(fitvec)
    axes = ellipse_axis_length(fitvec)

    if plot:    # Generate a diagnostic plot of the fitting result
        a, b = axes
        R = np.arange(0, 2*np.pi, 0.01)
        x = center[0] + a*np.cos(R)*np.cos(phi) - b*np.sin(R)*np.sin(phi)
        y = center[1] + a*np.cos(R)*np.sin(phi) + b*np.sin(R)*np.cos(phi)

        fsize = kwds.pop('figsize', (6, 6))
        f, ax = plt.subplots(figsize=fsize)
        try:
            ax.imshow(img, origin='lower', cmap='terrain_r')
        except:
            raise ValueError('Need to supply an image for plotting!')
        ax.scatter(rcoords, ccoords, 15, 'k')
        ax.plot(x, y, color = 'red')

    return center, phi, axes
