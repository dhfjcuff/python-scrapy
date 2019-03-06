import pymongo


class MongoDBPipeline(object):
    """
    1、连接数据库操作
    """

    def __init__(self, mongourl, mongoport, mongodb):
        '''
        初始化mongodb数据的url、端口号、数据库名称
        :param mongourl:
        :param mongoport:
        :param mongodb:
        '''
        self.mongourl = mongourl
        self.mongoport = mongoport
        self.mongodb = mongodb

    @classmethod
    def from_crawler(cls, crawler):
        """
        1、读取settings里面的mongodb数据的url、port、DB。
        :param crawler:
        :return:
        """
        return cls(
            mongourl=crawler.settings.get("MONGO_URL"),
            mongoport=crawler.settings.get("MONGO_PORT"),
            mongodb=crawler.settings.get("MONGO_DB")
        )

    def open_spider(self, spider):
        '''
        1、连接mongodb数据
        :param spider:
        :return:
        '''
        self.client = pymongo.MongoClient(self.mongourl, self.mongoport)
        self.db = self.client[self.mongodb]

    def process_item(self, item, spider):
        '''
        1、将数据写入数据库
        :param item:
        :param spider:
        :return:
        '''
        name = item.__class__.__name__
        # self.db[name].insert(dict(item))
        self.db['user'].update({'url_token': item['url_token']}, {'$set': item},
                               True)
        return item

    def close_spider(self, spider):
        '''
        1、关闭数据库连接
        :param spider:
        :return:
        '''
        self.client.close()