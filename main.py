from datetime import datetime
import json
import operator
import requests
import sys
from collections import deque

from tornado.httpclient import AsyncHTTPClient
from tornado.web import asynchronous
import tornado.ioloop
import tornado.web

# globals
network = {}
n_videos = 100

video_requests = []
video_queue = deque(video_requests)

# parameters
max_results = 25
pages = 10
start_date = 0
end_date = 0
completed = False

new_request = False
n_requests = 0

new_search_key = str(datetime.now())




""" Available functions:

    all posted objects should have the properties:
    - 'function': specifies the function to be performed.
    - 'input': input object
    - 'videos': number of videos to return

    expand: given a seed set of videos, expand to related videos

    'search' object example:
    {
        'function': 'search',
        'input': {
            'seed': ['adidas', 'basketball', 'shoes']
        }
        'count': 1000
    }

    expand object example:
    {
        'function': 'expand',
        'input': {
            'seed': ['1928398123', '1289371923', '8912739172']
        }
        'count': 1000
    }

"""


def videos_to_string(net):

    videos = sorted(net.iteritems(), key=operator.itemgetter(1))
    import json
    
    ll = []
    for video, count in videos:
        ll.append({
            'id': video,
            'relevancy': count
        })

    return str(json.dumps(ll))



def related_search(response, client, search_key):

    global n_requests
    n_requests -= 1

    global new_search_key

    if len(network) < n_videos:

        related_result = json.loads(response.body)

        video_ids = [r['id'] for r in related_result['data']['items']]
        for index, r in enumerate(related_result['data']['items']):

            sys.stdout.write('\b')
            sys.stdout.flush()
            sys.stdout.write('  %d videos found\r' % len(network))

            if r['id'] in network:
                network[r['id']] += 1
            elif len(network) < n_videos:
                network[r['id']] = 1
                http_client = AsyncHTTPClient()
                cb = lambda x: related_search(x, client, search_key)
                http_client.fetch("http://gdata.youtube.com/feeds/api/videos/{}/related?alt=jsonc&v=2".format(r['id']),
                                  callback=cb)
                n_requests += 1

    elif search_key == new_search_key:
        global completed
        if completed == False:
            completed = True


            try:
                client.write(videos_to_string(network))
                client.finish()
            except:
                client.finish()
                pass

            sys.stdout.write('\b')
            sys.stdout.flush()
            sys.stdout.write('  %d videos found\r' % len(network))
        return
    else:
        pass



def search_related(video_id, client):
    network = {}

    global n_requests
    global new_search_key
    new_search_key = str(datetime.now())

    http_client = AsyncHTTPClient()
    cb = lambda x: related_search(x, client, new_search_key)
    http_client.fetch("http://gdata.youtube.com/feeds/api/videos/{}/related?alt=jsonc&v=2".format(video_id),
                      callback=cb)
    n_requests += 1


def search_related(video_ids, client):
    network = {}
    global n_requests

    global new_search_key
    new_search_key = str(datetime.now())

    print "Launching The Spiderman on {0}.".format(search_query)
    done = False

    for video_id in video_ids:

        sys.stdout.write('\b')
        sys.stdout.flush()
        sys.stdout.write('  %d\r' % len(network))

        http_client.fetch("http://gdata.youtube.com/feeds/api/videos/{}/related?alt=jsonc&v=2".format(video_id),
                          callback=cb)

        http_client = AsyncHTTPClient()
        cb = lambda x: related_search(x, client, new_search_key)
        http_client.fetch(request_url, callback=cb)
        n_requests += 1



def search(keywords, client):
    network = {}
    global n_requests

    global new_search_key
    new_search_key = str(datetime.now())

    search_query = "+".join(keywords)
    search_query = search_query.replace(' ', '+')

    print "Launching The Spiderman on {0}.".format(search_query)
    done = False

    for start_index in range(1, pages):

        sys.stdout.write('\b')
        sys.stdout.flush()
        sys.stdout.write('  %d\r' % len(network))

        request_url = "http://gdata.youtube.com/feeds/api/videos?q={0}&orderby=relevance&alt=jsonc&v=2&max-results={1}&start-index={2}".format(
                search_query,
                max_results,
                start_index*25)

        http_client = AsyncHTTPClient()
        cb = lambda x: related_search(x, client, new_search_key)
        http_client.fetch(request_url, callback=cb)
        n_requests += 1


def on_fetch(response):

    if len(network) < n_videos:
        related_result = json.loads(response.body)
        video_ids = [r['id'] for r in related_result['data']['items']]


        spider(video_ids)
    else:
        return


def spider(feed):


    if len(network) < n_videos:

        videos = feed
        related = [0] * 25 * (len(videos)-1)

        for (i, video_id) in enumerate(videos):

            try:
                network[video_id] += 1
            except:
                network[video_id] = 0
                http_client = AsyncHTTPClient()
                try:
                    http_client.fetch("http://gdata.youtube.com/feeds/api/videos/{}/related?alt=jsonc&v=2".format(video_id),
                                      callback=on_fetch)
                except:
                    pass

    else:
        return


class ResultsHandler(tornado.web.RequestHandler):
    
    def get(self):
        done = False

        import operator

        videos = sorted(network.iteritems(), key=operator.itemgetter(1))
        print "first 50 elements:"
        print videos[:50]
        print "------------------"
        print "last 50 elements:"
        print videos[len(videos)-50:]


        new_file = open('videos.dict', 'w+')
        for entry in videos:
            new_file.write(entry[0] + ':' + str(entry[1]) + '\n')
        new_file.close( )

        import json
        # return json.dumps(videos)
        return_str = ''
        for v, count in videos:
            new_str = "http://www.youtube.com/video/{}".format(v)
            return_str += new_str + '\n'
        self.write(return_str)



class MainHandler(tornado.web.RequestHandler):


    @asynchronous
    def post(self):
        from spiderman import *

        import json
        post_request = json.loads(self.request.body)
        print "POST request"

        # parse POST request
        new_post_request = {
            'function': 'search',
            'input': {
                'seed': ['beats', 'dr dre', 'headphones', 'noise cancelling']
            },
            'count': 100
        }

        function_name = post_request['function']
        print function_name

        handler = Spiderman.get_handler(function_name)

        global tornado_loop

        spiderman = handler(self, post_request, tornado_loop).search()

        return


    def get(self):
        self.render('index.html', some_var="Hey Marc!")



application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/results", ResultsHandler)
])


def handle_request(response):
    if response.error:
        print "Error:", response.error
    else:
        print response.body


tornado_loop = []

if __name__ == "__main__":
    import os
    application.listen(os.environ.get("PORT", 5000))
    tornado_loop = tornado.ioloop.IOLoop.instance().start()



