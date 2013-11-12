import tornado.ioloop
import requests
from tornado.web import asynchronous
from tornado.httpclient import AsyncHTTPClient
import tornado.web
import json
import sys

network = {}

n_videos = 1000

# parameters
max_results = 25
pages = 2

def related_search(response):

    if len(network) < n_videos:

        related_result = json.loads(response.body)

        video_ids = [r['id'] for r in related_result['data']['items']]
        for index, r in enumerate(related_result['data']['items']):
            print r['id'], " ",
            if r['id'] in network:
                network[r['id']] += 1
            else:
                network[r['id']] = 1
                http_client = AsyncHTTPClient()
                http_client.fetch("http://gdata.youtube.com/feeds/api/videos/{}/related?alt=jsonc&v=2".format(r['id']),
                                  callback=related_search)

    else:
        return


def search(keywords):
    network = {}
    search_query = "+".join(keywords)
    search_query.replace(' ', '+')

    print "Launching The Spiderman on {0}.".format(search_query)
    for start_index in range(1, pages):
        request_url = "http://gdata.youtube.com/feeds/api/videos?q={0}&orderby=viewCount&alt=jsonc&v=2&max-results={1}&start-index={2}".format(
                search_query,
                max_results,
                start_index)

        http_client = AsyncHTTPClient()
        http_client.fetch(request_url, callback=related_search)


def on_fetch(response):

    if len(network) < n_videos:
        related_result = json.loads(response.body)
        video_ids = [r['id'] for r in related_result['data']['items']]


        spider(video_ids)
    else:
        return


def spider(feed):

    print len(network)

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

        return None

class MainHandler(tornado.web.RequestHandler):

    @asynchronous
    def get(self):

        search(['adidas', 'shoes', 'basketball'])
        return


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
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

