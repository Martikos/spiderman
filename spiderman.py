# Core imports 
from datetime import datetime
import json
import operator
import sys

# 3rd Party Imports
from tornado.httpclient import AsyncHTTPClient


def post():
    post_request = post_request

    function_name = post_request['name']

    handler = Spiderman.get_handler(function_name)
    spiderman = handler(self, post_request).search()


pages = 2
max_results = 100




class Spiderman(object):
    """Handles the searching.
    """

    def __init__(self, client, post_request, tornado_loop):
        self.tornado_loop = tornado_loop
        self.client = client
        self.video_count = post_request['count']
        self.number_of_requests = 0
        self.function_name = post_request['function']
        self.input_object = post_request['input']
        self.network = {}
        self.completed = False


    @classmethod
    def get_handler(cls, function_name):
        subs = cls.__subclasses__()
        subs.reverse()

        for sub in subs:
            if sub.can_handle_function(function_name):
                return sub
            else:
                raise Exception("No handler for function: %s" % function_name)


    @classmethod
    def can_handle_function(cls, function_name):
        if function_name is None or function_name is '':
            return None
        if hasattr(cls, 'functions'):
            return function_name in cls.functions


    @property
    def results_json(self):

        videos = sorted(self.network.iteritems(), key=operator.itemgetter(1))

        ll = []
        for video, count in videos:
            ll.append({
                'id': video,
                'relevancy': count
            })

        return str(json.dumps(ll))


    def related_search(self, response, request_index):
        if request_index == self.expected:
            print "done"
            print self.network

        self.some_number += 1
        print 'related search call: ', self.some_number

        boom = False

        related_videos = json.loads(response.body)
        video_ids = [r['id'] for r in related_videos['data']['items']]

        related_search = self.related_search
        http_client = AsyncHTTPClient()

        for index, video_id in enumerate(video_ids):

            if video_id in self.network:
                self.network[video_id] += 1
            else:
                self.network[video_id] = 1

            # if self.requested_videos < self.max_videos\
            #         and len(self.network) < self.max_videos:
            if self.requested_videos < self.expected:

                # Everytime this is called response has 25 videos.
                self.requested_videos += 1
                requested_videos = self.requested_videos
                print self.requested_videos, self.expected

                # print "making request"
                cb = lambda x: related_search(x, requested_videos)
                http_client.fetch("http://gdata.youtube.com/feeds/api/videos/{}/related?alt=jsonc&v=2".format(video_id),
                                  callback=cb)
            else:
                boom = True

        if boom == True:
            if self.done == False:
                self.done = True
                print len(self.network)

        if len(self.network) > self.video_count:
            print "done"



        # boom = False
        # print len(self.network), self.video_count, self.some_number

        # if len(self.network) < self.video_count:

        #     related_result = json.loads(response.body)
        #     video_ids = [r['id'] for r in related_result['data']['items']]

        #     related_search = self.related_search

        #     cb = lambda x: related_search(x)
        #     http_client = AsyncHTTPClient()

        #     for index, r in enumerate(related_result['data']['items']):


        #         if r['id'] in self.network:
        #             self.network[r['id']] += 1
        #         else:
        #             self.network[r['id']] = 1

        #         if self.some_number < self.video_count:
        #             self.network[r['id']] = 1

        #             q_s = "http://gdata.youtube.com/feeds/api/videos/{}/related?alt=jsonc&v=2".format(r['id'])
        #             self.some_number += 25
        #             http_client.fetch("http://gdata.youtube.com/feeds/api/videos/{}/related?alt=jsonc&v=2".format(r['id']),
        #                               callback=cb)

        #         else:
        #             boom = True

        # if boom:
        #     print len(self.network)
        #     print "should go in here right?"
        #     if self.completed == False:
        #         self.completed = True
        #         self.related_search = None
                
        #         try:
        #             self.client.write(self.results_json)
        #             self.client.finish()
        #         except:
        #             self.client.finish()
        #             pass

        #         del self.http_client
        #     else:
        #         self.left -= 1


        #     return


    def search():
        return NotImplemented



class SeedSearch(Spiderman):
    """Searches YouTube using keywords/query.
    """

    functions = 'search'

    def search(self):

        self.some_number = 0
        self.requested_videos = 0
        self.left = 0
        self.done = False

        self.network = {}
        from math import pow, ceil, floor, log
        self.max_videos = pow(25, ceil(log(self.video_count, 25)))
        self.expected = floor(self.video_count * 1.0 / 25)

        # callback function parameters
        search_key = self.search_key = str(datetime.now())
        related_search = self.related_search
        client = self.client
        cb = lambda x: related_search(x, 0)

        keywords = self.input_object['seed']
        search_query = '+'.join(keywords).replace(' ', '+')

        global pages
        global max_results

        self.http_client = AsyncHTTPClient()

        # Start crawling
        for start_index in range(1, pages):
            request_url = "http://gdata.youtube.com/feeds/api/videos?q={0}&orderby=relevance&alt=jsonc&v=2&max-results={1}&start-index={2}".format(
                    search_query,
                    max_results,
                    start_index*25)
            self.http_client.fetch(request_url, callback=cb)



