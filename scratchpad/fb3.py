import json
from geopy import geocoders
from os.path import exists
from django.contrib.gis.geos import fromstr as geo_from_str
from gheat_demo.friends.models import FriendPoint

if __name__ == "__main__":
    if exists('/Users/mtigas/Code/heatmap-mt/fb.cache.json'):
        f = open('/Users/mtigas/Code/heatmap-mt/fb.cache.json','r')
        cache = json.loads(f.read())
        f.close()
    else:
        cache = {}
     
    f = open('/Users/mtigas/Code/heatmap-mt/friends2.json','r')
    j = json.loads(f.read())
    f.close()

    geocoder = geocoders.Google('key')


    # Iterate over all f
    for f_id in j:
        friend = j[f_id]
        if friend.has_key('location'):
            if friend['location'].has_key('name'):
                if friend['location']['name']:
                    if cache.has_key(friend['location']['name']):
                        coord = cache[friend['location']['name']]
                    else:
                        place, (lat,lon) = geocoder.geocode(friend['location']['name'])
                        coord = (lon,lat)
                        cache[friend['location']['name']] = coord
                    p = FriendPoint(
                        name=u"%s" % f_id,
                        geometry=geo_from_str('POINT(%s %s)' % (coord[0],coord[1]))
                    )
                    p.save()
                    p.name = u"friend %s" % p.pk
                    p.save()
