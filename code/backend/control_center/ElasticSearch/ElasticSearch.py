from elasticsearch_dsl import connections
from elasticsearch_dsl import Search

class _ElasticSearchService:

    def __init__(self):
        self.__tweets = Search(index='tweets')
        self.__users = Search(index='users')
        self.__tweetstats = Search(index='tweetstats')
        self.__userstats = Search(index='userstats')

    def getAllStatsTweets(self,start = 0,length = 10):
        response = self.__tweetstats.query("match_all", **{})[start:start+length].execute()

        hits = []

        for hit in response.hits:
            dictionary = {}
            for key in hit:
                dictionary[key] = hit[key]
            hits.append(dictionary)
        
        return hits

def getESService():
    return _ElasticSearchSingleton

connections.create_connection(hosts=['192.168.85.46:9200'],timeout=20)
_ElasticSearchSingleton = _ElasticSearchService()

if __name__ == "__main__":
    es = getESService()
    tweetstats = es.getAllStatsTweets()
    print(tweetstats)
    tweetstats = es.getAllStatsTweets()
    print(tweetstats)