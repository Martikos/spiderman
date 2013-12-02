# Core imports 
from datetime import datetime
import json
import operator
import sys

# 3rd Party Imports
from tornado.httpclient import AsyncHTTPClient


pages = 10
max_results = 50


class Spiderman(object):
    """Handles the searching.
    """

    def __init__(self, client, post_request, tornado_loop):
        self.tornado_loop = tornado_loop
        self.client = client
        self.video_count = int(post_request['count'])
        self.number_of_requests = 0
        self.function_name = str(post_request['function'])
        self.input_object = post_request['input']
        self.identifier = post_request['identifier']
        self.network = {}
        self.completed = False


    @classmethod
    def get_handler(cls, function_name):
        subs = cls.__subclasses__()
        subs.reverse()
        import pdb; pdb.set_trace()

        for sub in subs:
            print sub.functions
            if sub.can_handle_function(function_name):
                return sub
        else:
            raise Exception("No handler for function: %s" % function_name)


    @classmethod
    def can_handle_function(cls, function_name):
        if function_name is None or function_name is '':
            return None
        if hasattr(cls, 'functions'):
            print cls.functions
            return function_name in cls.functions


    def write_to_db(self):
        from db import Video
        mongo_videos = []

        videos = sorted(self.network.iteritems(), key=operator.itemgetter(1))
        for video_id, meta in videos:
            try:
                mongo_video = Video(
                        campaign_id=self.campaign_id,
                        youtube_id=video_id,
                        used=True)
                mongo_video.save()
            except:
                pass

    @property
    def results_json(self):

        videos = sorted(self.network.iteritems(), key=operator.itemgetter(1))
        print videos

        ll = []
        for video_id, meta in videos:
            try:
                ll.append('http://www.youtube.com/video/{0}: {1}'.format(video_id, meta['title']))
            except:
                pass
            # ll.append({
            #     'id': video_id,
            #     'meta': {
            #         'relevancy': meta['relevancy'],
            #         'depth': meta['depth']
            #     }
            # })




        # return str(json.dumps(ll))
        return ('\n'.join(ll))


    def related_search(self, response, depth):
        self.requests_made -= 1

        boom = False

        related_videos = json.loads(response.body)
        video_ids = [(r['id'], r['title']) for r in related_videos['data']['items']]

        related_search = self.related_search
        http_client = AsyncHTTPClient()

        for index, (video_id, title) in enumerate(video_ids):

            if video_id in self.network:
                self.network[video_id]['relevancy'] += 1
            else:
                self.network[video_id] = {
                        'relevancy': 1,
                        'title': title,
                        'depth': depth
                }

            # if self.requested_videos < self.max_videos\
            #         and len(self.network) < self.max_videos:
            if len(self.network) < self.video_count:

                self.requests_made += 1
                cb = lambda x: related_search(x, depth+1)
                http_client.fetch("http://gdata.youtube.com/feeds/api/videos/{}/related?alt=jsonc&v=2".format(video_id),
                                  callback=cb)
            else:
                boom = True

        if boom == True:
            if self.done == False:
                self.done = True

        if self.requests_made == 0 and len(self.network) >= self.video_count:
            self.client.write(str(self.results_json))
            self.client.finish()


    def search():
        return NotImplemented


class ExpandSearch(Spiderman):
    """Expands youtube video network.
    """

    functions = 'expand'

    def search(self):

        self.done = False
        self.requests_made = 1
        self.network = {}

        # callback function parameters
        search_key = self.search_key = str(datetime.now())
        related_search = self.related_search
        client = self.client

        cb = lambda x: related_search(x, 0)

        video_ids = [str(k) for k in self.input_object['seed']]

        global pages
        global max_results

        self.http_client = AsyncHTTPClient()

        for video_id in video_ids:
            self.http_client.fetch("http://gdata.youtube.com/feeds/api/videos/{}/related?alt=jsonc&v=2".format(video_id),
                              callback=cb)





class SeedSearch(Spiderman):
    """Searches YouTube using keywords/query.
    """

    functions = 'search'

    def search(self):

        self.done = False
        self.requests_made = 1

        # callback function parameters
        search_key = self.search_key = str(datetime.now())
        related_search = self.related_search
        client = self.client

        cb = lambda x: related_search(x, 0)

        keywords = [str(k) for k in self.input_object['seed']]
        search_query = '+'.join(keywords).replace(' ', '+')

        global pages
        global max_results

        self.http_client = AsyncHTTPClient()

        for start_index in range(1, pages):
            request_url = "http://gdata.youtube.com/feeds/api/videos?q={0}&orderby=relevance&alt=jsonc&v=2&max-results={1}&start-index={2}".format(
                    search_query,
                    max_results,
                    start_index*25)
            self.http_client.fetch(request_url, callback=cb)



