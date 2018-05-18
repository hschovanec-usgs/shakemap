#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 16:40:33 2018

@author: hschovanec
"""
from impactutils.vectorutils.ecef import ecef2latlon, latlon2ecef
from impactutils.vectorutils.vector import Vector
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from openquake.hazardlib.geo.geodetic import point_at

def getMinorPoints(P, corner, dx, dy, strike, dip):
    # Get dip direction minor point
    direction = dip
    distance = dy
    dip_min = {}
    dip_min['lon'], dip_min['lat'] = point_at(corner['lat'], corner['lon'], direction, distance)
    dip_min['depth'] = P['depth']
    
    # Get strike direction minor point
    direction = strike
    distance = dx
    strike_min = {}
    strike_min['lon'], strike_min['lat'] = point_at(corner['lat'], corner['lon'], direction, distance)
    strike_min['depth'] = corner['depth']
    return strike_min, dip_min
    
    
    
    


def getFourCorners(instance):
    dip = instance['dip']
    strike = instance['strike']
    dx = instance['dx']
    dy = instance['dy']
    p_lat = instance['point']['lat']
    p_lon = instance['point']['lon']
    
    dip = np.deg2rad(dip)
    theta = np.rad2deg(np.arctan(dy / dx))
    direction = strike + 180 + theta
    distance = np.sqrt( dx**2 + (dy * np.sin(dip))**2)
    P1 = {}
    P1['lon'] , P1['lat'] = point_at(p_lon, p_lat, direction, distance)
    h1 = instance['point']['depth'] - np.abs(dy * np.cos(dip))
    P1['depth'] = h1
    
    strike_min, dip_min = getMinorPoints(instance['point'], P1, dx, dy, strike, np.rad2deg(dip))
    
    # convert to ECEF
    P1x, P1y, P1z = latlon2ecef(P1['lat'], P1['lon'], P1['depth'])
    stx, sty, stz = latlon2ecef(strike_min['lat'], strike_min['lon'], 
                             strike_min['depth'])
    dpx, dpy, dpz = latlon2ecef(dip_min['lat'], dip_min['lon'], dip_min['depth'])
    
    # Get strike vector
    P1_vec = Vector(P1x, P1y, P1z)
    st_vec = Vector(stx, sty, stz)
    dp_vec = Vector(dpx, dpy, dpz)
    
    # Get vector between two
    dip_direction = P1_vec.cross(dp_vec)
    print(dip_direction.x, dip_direction.y, dip_direction.z)
    
    strike_direction = P1_vec.cross(st_vec)
    print(strike_direction.x, strike_direction.y, strike_direction.z)
    
    dd = strike_direction.dot(dip_direction)
    print(dd)
    
    
    
    
    

    return P1, strike_min, dip_min


instance = {}
instance['point'] = {}
instance['point']['lat'] = 3
instance['point']['lon'] = -179.921526
instance['point']['depth'] = 5
instance['dx'] = 200
instance['dy'] = 200
instance['width'] = 500
instance['length'] = 500
instance['strike'] = 0
instance['dip'] = 30

P1, strike_min, dip_min = getFourCorners(instance)
z = np.array([P1['depth'], strike_min['depth'], dip_min['depth']])
x = np.array([P1['lat'], strike_min['lat'], dip_min['lat']])
y = np.array([P1['lon'], strike_min['lon'], dip_min['lon']])

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(x, y, z)
ax.scatter([instance['point']['lat']], [instance['point']['lon']], [instance['point']['depth']])
#ax.legend()
ax.set_xlabel("Latitude")
ax.set_ylabel("Longitude")
ax.set_zlabel("Depth")

plt.show()
