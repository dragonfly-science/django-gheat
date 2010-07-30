from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.contrib.gis.geos import fromstr as geo_from_str

import urllib2
import json
import os

from gheat_demo.tweetmap.models import TweetPoint

class Command(NoArgsCommand):
    help = "Collects dummy TweetPoint data from the Twitter Stream API."

    output_transaction = True

    def handle_noargs(self, **options):
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        top_level_url = "http://stream.twitter.com/"
        password_mgr.add_password(None, top_level_url, getattr(settings,'TWITTER_USERNAME',''), getattr(settings,'TWITTER_PASSWORD',''))
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        f = opener.open("http://stream.twitter.com/1/statuses/sample.json")
        
        for line in f:
            data = json.loads("[%s]"%line)
            tweet = data[0]
            
            # http://dev.twitter.com/doc/get/statuses/public_timeline
            # for example tweet payload
            if tweet.has_key('id') and tweet.has_key('geo') and tweet['geo']:
                strval = "https://twitter.com/%s/status/%s" % (
                    tweet['user']['screen_name'],
                    tweet['id'],
                )
                latitude = tweet['geo']['coordinates'][0]
                longitude = tweet['geo']['coordinates'][1]
                coordstr = "POINT(%s %s)" % (longitude, latitude)
                p = TweetPoint(
                    name=u"%s" % strval,
                    geometry=geo_from_str(coordstr)
                )
                p.save()
                print p.name
                print coordstr
                print
        
        f.close()