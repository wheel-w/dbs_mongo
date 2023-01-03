from rest_framework import serializers
from rest_framework.fields import DictField


class ListCollectionNamesSerializer(serializers.Serializer):
    db_name = serializers.CharField(label="数据库名称", required=True)


class SortKwargsSerializer(serializers.Serializer):
    field_name = serializers.CharField(label="排序字段名", required=True)
    sort_type = serializers.ChoiceField(label="排序类型", choices=[-1, 1], required=True)


class DocumentQuerySerializer(serializers.Serializer):
    db_name = serializers.CharField(label="数据库名称", required=True)
    collection_name = serializers.CharField(label="集合名称", required=True)
    page = serializers.IntegerField(label="分页页码", default=1)
    page_size = serializers.IntegerField(label="每页数量", default=10)
    query_kwargs = serializers.DictField(label="分页条件", default={})
    hide_field_list = serializers.ListField(label="隐藏不返回字段", default=[])
    sort_kwargs_list = serializers.ListField(label="排序字段", child=SortKwargsSerializer(), default=[])


class DocumentInsertOneSerializer(serializers.Serializer):
    db_name = serializers.CharField(label="数据库名称", required=True)
    collection_name = serializers.CharField(label="集合名称", required=True)
    insert_kwargs = serializers.DictField(label="文档插入内容")


class DocumentInsertManySerializer(serializers.Serializer):
    db_name = serializers.CharField(label="数据库名称", required=True)
    collection_name = serializers.CharField(label="集合名称", required=True)
    insert_kwargs_list = serializers.ListField(label="文档插入多行数据列表", child=DictField())


class DocumentDeleteSerializer(serializers.Serializer):
    db_name = serializers.CharField(label="数据库名称", required=True)
    collection_name = serializers.CharField(label="集合名称", required=True)
    delete_kwargs = serializers.DictField(label="删除查询条件")


class DocumentUpdateSerializer(serializers.Serializer):
    db_name = serializers.CharField(label="数据库名称", required=True)
    collection_name = serializers.CharField(label="集合名称", required=True)
    update_query_kwargs = serializers.DictField(label="更新查询条件")
    update_new_kwargs = serializers.DictField(label="更新后的值")
