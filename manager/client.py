import logging

import pymongo
from pymongo.errors import PyMongoError

from manager.models import MongoInstance

logger = logging.getLogger("mongo")


class DbsMongoClient:
    def __init__(self, instance_id=None, instance_kwargs=None):
        self.instance_id = instance_id
        self.instance_kwargs = instance_kwargs
        self.client = None

    def __enter__(self):
        client_kwargs = {}
        if self.instance_id:
            instance = MongoInstance.objects.get_instance(self.instance_id)
            client_kwargs = {
                "host": instance.db_host,
                "port": instance.db_port,
                "username": instance.db_user,
                "password": instance.plain_password,
                "authSource": instance.auth_source,
                "authMechanism": instance.auth_mechanism,
            }
        if self.instance_kwargs:
            client_kwargs = {
                "host": self.instance_kwargs.get("db_host"),
                "port": self.instance_kwargs.get("db_port"),
                "username": self.instance_kwargs.get("db_user"),
                "password": self.instance_kwargs.get("db_password"),
                "authSource": self.instance_kwargs.get("auth_source"),
                "authMechanism": self.instance_kwargs.get("auth_mechanism"),
            }
        self.client = pymongo.MongoClient(**client_kwargs)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()
        return False

    def test_connection(self):
        try:
            self.client.server_info()
        except PyMongoError as e:
            logger.exception("Mongo instance connect fail!")
            return False, repr(e)

        return True, "Connection Success!"

    def list_database_names(self):
        """
        获取数据库列表
        :return: ['admin', 'config', 'local']
        """
        return self.client.list_database_names()

    def list_collection_names(self, db_name):
        """
        获取当前数据库下的所有集合
        :return:['system.keys', 'system.users', 'cmongo_test']
        """
        current_db = self.client[db_name]
        return current_db.list_collection_names()

    def page_query(self, db_name, collection_name, query_kwargs={}, page=1, page_size=10):
        """
        查询文档
        :param db_name:
        :param collection_name:
        :param query_kwargs:
        :param page:
        :param page_size:
        :return:
        """
        current_db = self.client[db_name]
        current_collection = current_db[collection_name]

        skip = page_size * (page - 1)
        query_result = current_collection.find(query_kwargs).limit(page_size).skip(skip)
        data = [item for item in query_result]

        return data

    def command(self, db_name, command):
        """
        执行mongodb原生命令
        :param db_name:
        :param command:
        :return:
        """
        current_db = self.client[db_name]
        return current_db.command(command)
