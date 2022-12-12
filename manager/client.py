import logging

import pymongo
from pymongo.errors import PyMongoError

from manager.models import MongoInstance

logger = logging.getLogger("mongo")


class DbsMongoClient:
    def __init__(self, instance_id):
        self.instance = MongoInstance.objects.get_instance(instance_id)
        self.client = pymongo.MongoClient(
            host=self.instance.db_host,
            port=self.instance.db_port,
            username=self.instance.db_user,
            password=self.instance.plain_password,
            authSource=self.instance.auth_source,
            authMechanism=self.instance.auth_mechanism,
        )

    @staticmethod
    def test_connection(instance_kwargs):
        try:
            test_client = pymongo.MongoClient(
                host=instance_kwargs.get("db_host"),
                port=instance_kwargs.get("db_port", 27017),
                username=instance_kwargs.get("db_user", ""),
                password=instance_kwargs.get("db_password", ""),
                authSource=instance_kwargs.get("auth_source", "admin"),
                authMechanism=instance_kwargs.get("auth_mechanism", "DEFAULT"),
            )
            test_client.server_info()
        except PyMongoError:
            logger.exception("连接mongo失败,请检查连接信息")
            return False

        return True

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
