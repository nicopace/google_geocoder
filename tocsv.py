from geocode import Address, depickleit

pickle_file = "status.pickle"
status_dict = depickleit(pickle_file)

for addr, lat, lon in status_dict['locations']:
    print "%s, %s, %s" % (addr.addr, lon, lat)
