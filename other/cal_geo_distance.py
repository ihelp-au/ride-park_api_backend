# Calculate geo distance between two coordinates
from geopy.distance import geodesic


# Sydney Airport
coord_syd_apt = (-33.939980, 151.174919)

# Sydney Opera
coord_syd_opr = (-33.902854, 151.0827897)


distance: float = geodesic(coord_syd_apt, coord_syd_opr).km

print(f"""Distance between Sydney Airport {coord_syd_apt} and
      Sydney Opera {coord_syd_opr} is {distance} km
""")
