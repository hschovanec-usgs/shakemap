#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 14:05:54 2018

@author: hschovanec
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from openquake.hazardlib.geo.geodetic import point_at
import matplotlib.ticker as mticker
import cartopy.crs as ccrs

from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER







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
    
    direction = strike
    distance = instance['length']
    P2 = {}
    P2['lon'] , P2['lat'] = point_at(P1['lon'] , P1['lat'], direction, distance)
    P2['depth'] = h1
    
    direction = strike + 90
    distance = instance['width'] * np.cos(dip)
    P3 = {}
    P3['lon'] , P3['lat'] = point_at(P2['lon'] , P2['lat'], direction, distance)
    h2 = P1['depth'] + np.abs((instance['width']) * np.cos(dip))
    P3['depth'] = h2
    
    direction = strike + 180
    distance = instance['length']
    P4 = {}
    P4['lon'] , P4['lat'] = point_at(P3['lon'] , P3['lat'], direction, distance)
    h2 = P1['depth'] + np.abs((instance['width']) * np.cos(dip))
    P4['depth'] = h2

    return P1, P2, P3, P4


instance = {}
instance['point'] = {}
instance['point']['lat'] = 3
instance['point']['lon'] = -179.921526
instance['point']['depth'] = 5
instance['dx'] = 200
instance['dy'] = 200
instance['width'] = 500
instance['length'] = 500
instance['strike'] = 90
instance['dip'] = 30



P1, P2, P3, P4 = getFourCorners(instance)
z = np.array([P1['depth'], P2['depth'], P3['depth'], P4['depth'], P1['depth']])
x = np.array([P1['lat'], P2['lat'], P3['lat'], P4['lat'], P1['lat']])
y = np.array([P1['lon'], P2['lon'], P3['lon'], P4['lon'], P1['lon']])

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(x, y, z)
ax.scatter([instance['point']['lat']], [instance['point']['lon']], [instance['point']['depth']])
ax.legend()
ax.set_xlabel("Latitude")
ax.set_ylabel("Longitude")
ax.set_zlabel("Depth")

plt.show()

plt.figure()
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.plot(x, y, label='Corners')
plt.scatter([instance['point']['lat']], [instance['point']['lon']], [instance['point']['depth']], label='Known Point')
plt.legend()
plt.show()



ax = plt.axes(projection=ccrs.Mercator())
ax.coastlines()

gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=2, color='gray', alpha=0.5, linestyle='--')
gl.xlabels_top = False
gl.ylabels_left = False
gl.xlines = False
gl.xlocator = mticker.FixedLocator([-180, -45, 0, 45, 180])
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlabel_style = {'size': 15, 'color': 'gray'}
gl.xlabel_style = {'color': 'red', 'weight': 'bold'}

plt.show()


print(instance['point']['lat'], instance['point']['lon'])
print(P1['lat'], P1['lon'])
print(P2['lat'], P2['lon'])
print(P3['lat'], P3['lon'])
print(P4['lat'], P4['lon'])


array = [0,instance['dy'],instance['width']]
z = np.polyfit(array, [P1['depth'], instance['point']['depth'], P4['depth']], 1)
p = np.poly1d(z)
f = p(array)
plt.plot(array, f, linewidth=5)
plt.plot(array, [P1['depth'], instance['point']['depth'], P4['depth']])

print('Theoretical: ',p(instance['dy']))
print('Real: ', instance['point']['depth'])
