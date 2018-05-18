import numpy as np
import math
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import OrderedDict
from openquake.hazardlib.geo.geodetic import point_at


def point_at(lat, lon, bearing, distance):
    earth_radius = 6371.0088
    next_lat = np.rad2deg((distance / earth_radius) * np.cos(bearing)) + lat
    next_lon = np.rad2deg((distance / (earth_radius * np.sin(np.radians(next_lat)))) * np.sin(bearing)) + lon
    return next_lat, next_lon
    
def getOrigin(P, dx, dy, strike, dip):
    lat = P['lat']
    lon = P['lon'] 
    dip = np.deg2rad(dip)
    direction = np.deg2rad(strike - 45)
    distance = np.sqrt( dx**2 + (dy*np.sin(dip))**2)
    lat, lon = point_at(lat, lon, direction, distance)
    depth = P['depth'] - np.abs(dy * np.cos(dip))
    print(P['depth'] , depth)
    origin = OrderedDict()
    origin['lat'] = lat
    origin['lon'] = lon
    origin['depth'] = depth
    return origin

def getFourCorners(instance):
    dip = instance['dip']
    strike = instance['strike']
    
    dip = np.deg2rad(dip)
    theta = np.rad2deg(np.arctan(instance['dy'] / instance['dx']))
    direction = strike + 180 + theta
    distance = np.sqrt( instance['dx']**2 + (instance['dy']*np.sin(dip))**2)
    P1 = OrderedDict()
    P1['lon'] , P1['lat'] = point_at(instance['point']['lon'], instance['point']['lat'], direction, distance)

    
    # Get Upper Corner
    direction = strike
    distance = instance['length']
    P2 = OrderedDict()
    P2['lon'] , P2['lat'] = point_at(P1['lon'], P1['lat'], direction, distance)
    
    # Get Lower Corners
    direction = strike + 90
    distance = instance['width'] * np.sin(dip)
    P3 = OrderedDict()
    P3['lon'] , P3['lat'] = point_at(P2['lon'], P2['lat'], direction, distance)
    
    direction = strike + 180
    distance = instance['length']
    P4 = OrderedDict()
    P4['lon'] , P4['lat'] = point_at(P3['lon'], P3['lat'], direction, distance)
    
    h1 = instance['point']['depth'] - np.abs(instance['dy'] * np.cos(dip))
    P1['depth'] = h1
    P2['depth'] = h1
    
    h2 = P1['depth'] + np.abs((instance['width']) * np.cos(dip))
    P3['depth'] = h2
    P4['depth'] = h2
    return (P1, P2, P3, P4)



#def createGEOJSON(instance):
    

    
    
    


instance = {}
instance['point'] = {}
instance['point']['lat'] = -3.025115
instance['point']['lon'] = 37.929921
instance['point']['depth'] = 20
instance['dx'] = 3
instance['dy'] = 1
instance['width'] = 30
instance['length'] = 20
instance['strike'] = 10
instance['dip'] = 30



P1, P2, P3, P4 = getFourCorners(instance)
z = np.array([P1['depth'], P2['depth'], P3['depth'], P4['depth'], P1['depth']])
x = np.array([P1['lat'], P2['lat'], P3['lat'], P4['lat'], P1['lat']])
y = np.array([P1['lon'], P2['lon'], P3['lon'], P4['lon'], P1['lon']])

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(x, y, z, label='parametric curve')
ax.scatter([instance['point']['lat']], [instance['point']['lon']], [instance['point']['depth']])
ax.legend()
plt.show()

print(instance['point']['lat'], instance['point']['lon'])
print(P1['lat'], P1['lon'])
print(P2['lat'], P2['lon'])
print(P3['lat'], P3['lon'])
print(P4['lat'], P4['lon'])
"""print(instance['point']['lat'], instance['point']['lon'], instance['point']['depth'])
print(P1['lat'], P1['lon'], P1['depth'])
print(P2['lat'], P2['lon'], P2['depth'])
print(P3['lat'], P3['lon'], P3['depth'])
print(P4['lat'], P4['lon'], P4['depth'])"""
array = [0,instance['dy'],instance['width']]
z = np.polyfit(array, [P1['depth'], instance['point']['depth'], P4['depth']], 1)
p = np.poly1d(z)
f = p(array)
plt.plot(array, f, linewidth=5)
plt.plot(array, [P1['depth'], instance['point']['depth'], P4['depth']])

print('Theoretical: ',p(instance['dy']))
print('Real: ', instance['point']['depth'])




#print(P1, P2, P3, P4)
