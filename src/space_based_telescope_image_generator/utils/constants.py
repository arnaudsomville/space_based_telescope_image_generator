"""File where are store important constants."""

import math as m


earth_radius = 6378.0  # Rayon de la Terre en km
atmosphere_radius = earth_radius + 50
au_km = 1500000  # 1UA = 150Million km. Too far away for Povray so for object far away we will use 1UA = 1 500 000 km (scale 1:100)
earth_sun_distance = au_km  # 150 million km (1UA)
starmap_sphere_radius = 2 * au_km


MU = 3.986004418e14  # [m3/s2] Standard gravitational constant of the Earth
J2 = 1082.62668e-6  # [-] Perturbation constant from gravitational potential
RE = 6378.137e3  # [m] Equatorial radius of the Earth
DAY_SECONDS = 86400  # [s] Seconds in a solar day
PI = m.pi  # Pi

OBLIQUITY = m.radians(-23.45)  # [deg] Obliquity of the Earth about the ecliptic
