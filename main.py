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


def videos_to_string(net):

    videos = sorted(net.iteritems(), key=operator.itemgetter(1))

    return_str = ''
    for v, count in videos:
        new_str = "http://www.youtube.com/video/{}".format(v)
        return_str += new_str + '\n'
    return return_str


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
        new_file.close()

        import json
        # return json.dumps(videos)
        return_str = ''
        for v, count in videos:
            new_str = "http://www.youtube.com/video/{}".format(v)
            return_str += new_str + '\n'
        self.write(return_str)


class MainHandler(tornado.web.RequestHandler):

    @asynchronous
    def get(self):

        self.flush()


        global network
        network = {}

        global completed
        completed = False

        query_string = self.get_argument("keywords", None)
        global n_videos
        n_videos = int(self.get_argument("count", 100))

        keywords = str(query_string).split(' ')

        completed = False
        search(keywords, self)


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/results", ResultsHandler)
])


def handle_request(response):
    if response.error:
        print "Error:", response.error
    else:
        print response.body


if __name__ == "__main__":
    import os
    application.listen(os.environ.get("PORT", 5000))
    tornado.ioloop.IOLoop.instance().start()

