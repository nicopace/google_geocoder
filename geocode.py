import csv
import cPickle
import os
import geopy

from collections import namedtuple


def pickleit(obj, path):
    with open(path, "w") as f:
        cPickle.dump(obj, f)


def depickleit(path):
    with open(path, "rb") as f:
        return cPickle.load(f)
    return None

if __name__ == "__main__":
    Address = namedtuple('Address', 'addr, city, state, batch')

    status_dict = {
        "locations" : [],
        "errors" : [],
    }

    pickle_file = "status.pickle"
    if os.path.exists(pickle_file):
        status_dict = depickleit(pickle_file)

    csv_reader = csv.reader(open("cada300.csv", "rb"))

    # Skip header
    csv_reader.next()

    to_skip = len(status_dict["locations"])

    print "Skipping", to_skip
    for _ in xrange(to_skip):
        csv_reader.next()

    g = geopy.geocoders.GoogleV3()

    for addr in map(Address._make, csv_reader):
        try:
            print addr
            lat, lon = g.geocode("%s, %s, %s" % (addr.addr, addr.city, addr.state))
            status_dict["locations"].append((addr, lat, lon))
            print lat, lon
        except geopy.geocoders.googlev3.GQueryError as e:
            pickleit(status_dict, pickle_file)
            print "Caught a problem with the geoquery:", e
            print "Saving so far and quitting..."
            quit()
        except KeyboardInterrupt:
            pickleit(status_dict, pickle_file)
            print "Caught Ctrl+C. Saving so far and quitting..."
            quit()
        except Exception as e:
            print e
            status_dict["errors"].append((addr, e))
