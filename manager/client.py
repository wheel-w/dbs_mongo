import logging

import pymongo
from pymongo.errors import PyMongoError

from common.utils.bson import bson_to_json, json_to_bson
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

    def dispatch(self, method, *args, **kwargs):
        instance_id = self.instance_id or "UnAuth Instance"
        try:
            result = getattr(self, method)(*args, **kwargs)
        except PyMongoError as e:
            logger.exception("[{}] {}  fail!!!".format(instance_id, method))
            return False, repr(e)
        except Exception as ex:
            logger.exception("[{}] {} occur unexpected error!!!".format(instance_id, method))
            return False, repr(ex)

        return True, result

    def test_connection(self):
        """
        Test mongo instance connection
        """
        self.client.server_info()

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

    def document_query(
        self, db_name, collection_name, query_kwargs={}, sort_kwargs_list={}, hide_field_list=[], page=1, page_size=10
    ):
        """
        查询文档
        :param db_name:
        :param collection_name:
        :param query_kwargs:
        :param sort_kwargs_list:
        :param hide_field_list:
        :param page:
        :param page_size:
        :return:
        """
        current_db = self.client[db_name]
        current_collection = current_db[collection_name]
        query_kwargs = json_to_bson(query_kwargs)
        count = current_collection.count_documents(query_kwargs)

        field_kwargs = {f: 0 for f in hide_field_list}

        skip = page_size * (page - 1)
        cursor = current_collection.find(query_kwargs, field_kwargs)
        if sort_kwargs_list:
            for sort_kwargs in sort_kwargs_list:
                cursor = cursor.sort(sort_kwargs["field_name"], sort_kwargs["sort_type"])

        cursor = cursor.limit(page_size).skip(skip)
        bson_result = [item for item in cursor]
        data = {"count": count, "page": page, "list": bson_to_json(bson_result)}
        return data

    def document_insert_one(self, db_name, collection_name, insert_kwargs):
        """
        文档插入一条数据
        :param db_name:
        :param collection_name:
        :param insert_kwargs:
        :return:
        """
        current_db = self.client[db_name]
        current_collection = current_db[collection_name]
        insert_kwargs = json_to_bson(insert_kwargs)
        result = current_collection.insert_one(insert_kwargs)
        return {"_id": bson_to_json(result.inserted_id)}

    def document_insert_many(self, db_name, collection_name, insert_kwargs_list):
        """
        文档插入多行数据
        :param db_name:
        :param collection_name:
        :param insert_kwargs_list:
        :return:
        """
        current_db = self.client[db_name]
        current_collection = current_db[collection_name]
        insert_kwargs_list = json_to_bson(insert_kwargs_list)
        result = current_collection.insert_many(insert_kwargs_list)
        data = [{"_id": _id} for _id in bson_to_json(result.inserted_ids)]
        return data

    def document_delete_one(self, db_name, collection_name, delete_kwargs):
        """
        文档删除一条数据
        :param db_name:
        :param collection_name:
        :param delete_kwargs:
        :return:
        """
        current_db = self.client[db_name]
        current_collection = current_db[collection_name]
        delete_kwargs = json_to_bson(delete_kwargs)
        result = current_collection.delete_one(delete_kwargs)
        if result.deleted_count == 0:
            raise PyMongoError("Delete Count num is 0,Please check delete conditions")
        return {"deleted_count": result.deleted_count}

    def document_delete_many(self, db_name, collection_name, delete_kwargs):
        """
        文档删除多条数据
        :param db_name:
        :param collection_name:
        :param delete_kwargs:
        :return:
        """
        current_db = self.client[db_name]
        current_collection = current_db[collection_name]
        delete_kwargs = json_to_bson(delete_kwargs)
        result = current_collection.delete_many(delete_kwargs)
        if result.deleted_count == 0:
            raise PyMongoError("Delete Count num is 0,Please check delete conditions")
        return {"modified_count": result.deleted_count}

    def document_update_one(self, db_name, collection_name, update_query_kwargs, update_new_kwargs):
        """
        文档更新一条数据
        :param db_name:
        :param collection_name:
        :param update_query_kwargs:
        :param update_new_kwargs:
        :return:
        """
        current_db = self.client[db_name]
        current_collection = current_db[collection_name]
        update_query_kwargs = json_to_bson(update_query_kwargs)
        update_new_kwargs = json_to_bson(update_new_kwargs)
        result = current_collection.update_one(update_query_kwargs, update_new_kwargs)
        if result.modified_count == 0:
            raise PyMongoError("Modified Count num is 0,Please check modify conditions")
        return {"modified_count": result.modified_count}

    def document_update_many(self, db_name, collection_name, update_query_kwargs, update_new_kwargs):
        """
        文档多条一条数据
        :param db_name:
        :param collection_name:
        :param update_query_kwargs:
        :param update_new_kwargs:
        :return:
        """
        current_db = self.client[db_name]
        current_collection = current_db[collection_name]
        update_query_kwargs = json_to_bson(update_query_kwargs)
        update_new_kwargs = json_to_bson(update_new_kwargs)
        result = current_collection.update_many(update_query_kwargs, update_new_kwargs)
        if result.modified_count == 0:
            raise PyMongoError("Modified Count num is 0,Please check modify conditions")
        return {"modified_count": result.modified_count}
