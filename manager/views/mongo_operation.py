from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from manager.client import DbsMongoClient
from manager.decorators import operation_record
from manager.permissions.mongo_operation_permission import MongoOperationPermission
from manager.serializers.mongo_operation_serializer import (
    DocumentDeleteSerializer,
    DocumentInsertManySerializer,
    DocumentInsertOneSerializer,
    DocumentQuerySerializer,
    DocumentUpdateSerializer,
    ListCollectionNamesSerializer,
)


@method_decorator(operation_record, name="dispatch")
class MongoOperationViewSet(GenericViewSet):
    queryset = "xxx"
    serializer_class = DocumentQuerySerializer
    permission_classes = [MongoOperationPermission]

    @action(detail=True, methods=["GET"])
    def list_database_names(self, request, pk):
        with DbsMongoClient(instance_id=pk) as mongo_client:
            ok, data = mongo_client.dispatch("list_database_names")
        return Response(data, exception=not ok)

    @swagger_auto_schema(
        method="GET", operation_summary="list_collection_names", query_serializer=ListCollectionNamesSerializer
    )
    @action(detail=True, methods=["GET"])
    def list_collection_names(self, request, pk):
        serializer = ListCollectionNamesSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        db_name = serializer.data["db_name"]
        with DbsMongoClient(instance_id=pk) as mongo_client:
            ok, data = mongo_client.dispatch("list_collection_names", db_name)
        return Response(data, exception=not ok)

    @swagger_auto_schema(method="POST", operation_summary="document_query", request_body=DocumentQuerySerializer)
    @action(detail=True, methods=["POST"])
    def document_query(self, request, pk):
        serializer = DocumentQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        db_name = serializer.data["db_name"]
        collection_name = serializer.data["collection_name"]
        query_kwargs = serializer.data["query_kwargs"]
        page = serializer.data["page"]
        page_size = serializer.data["page_size"]
        hide_field_list = serializer.data["hide_field_list"]
        sort_kwargs_list = serializer.data["sort_kwargs_list"]
        with DbsMongoClient(instance_id=pk) as mongo_client:
            ok, data = mongo_client.dispatch(
                "document_query",
                db_name,
                collection_name,
                query_kwargs,
                sort_kwargs_list,
                hide_field_list,
                page,
                page_size,
            )
        return Response(data, exception=not ok)

    @swagger_auto_schema(
        method="POST", operation_summary="document_insert_one", request_body=DocumentInsertOneSerializer
    )
    @action(detail=True, methods=["POST"])
    def document_insert_one(self, request, pk):
        serializer = DocumentInsertOneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        db_name = serializer.data["db_name"]
        collection_name = serializer.data["collection_name"]
        insert_kwargs = serializer.data["insert_kwargs"]
        with DbsMongoClient(instance_id=pk) as mongo_client:
            ok, data = mongo_client.dispatch("document_insert_one", db_name, collection_name, insert_kwargs)

        return Response(data, exception=not ok)

    @swagger_auto_schema(
        method="POST", operation_summary="document_insert_many", request_body=DocumentInsertManySerializer
    )
    @action(detail=True, methods=["POST"])
    def document_insert_many(self, request, pk):
        serializer = DocumentInsertManySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        db_name = serializer.data["db_name"]
        collection_name = serializer.data["collection_name"]
        insert_kwargs_list = serializer.data["insert_kwargs_list"]
        with DbsMongoClient(instance_id=pk) as mongo_client:
            ok, data = mongo_client.dispatch("document_insert_many", db_name, collection_name, insert_kwargs_list)
        return Response(data, exception=not ok)

    @swagger_auto_schema(
        method="DELETE", operation_summary="document_delete_one", request_body=DocumentDeleteSerializer
    )
    @action(detail=True, methods=["DELETE"])
    def document_delete_one(self, request, pk):
        serializer = DocumentDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        db_name = serializer.data["db_name"]
        collection_name = serializer.data["collection_name"]
        delete_kwargs = serializer.data["delete_kwargs"]
        with DbsMongoClient(instance_id=pk) as mongo_client:
            ok, data = mongo_client.dispatch("document_delete_one", db_name, collection_name, delete_kwargs)

        return Response(data, exception=not ok)

    @swagger_auto_schema(
        method="DELETE", operation_summary="document_delete_many", request_body=DocumentDeleteSerializer
    )
    @action(detail=True, methods=["DELETE"])
    def document_delete_many(self, request, pk):
        serializer = DocumentDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        db_name = serializer.data["db_name"]
        collection_name = serializer.data["collection_name"]
        delete_kwargs = serializer.data["delete_kwargs"]
        with DbsMongoClient(instance_id=pk) as mongo_client:
            ok, data = mongo_client.dispatch("document_delete_many", db_name, collection_name, delete_kwargs)

        return Response(data, exception=not ok)

    @swagger_auto_schema(method="PUT", operation_summary="document_update_one", request_body=DocumentUpdateSerializer)
    @action(detail=True, methods=["PUT"])
    def document_update_one(self, request, pk):
        serializer = DocumentUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        db_name = serializer.data["db_name"]
        collection_name = serializer.data["collection_name"]
        update_query_kwargs = serializer.data["update_query_kwargs"]
        update_new_kwargs = serializer.data["update_new_kwargs"]
        with DbsMongoClient(instance_id=pk) as mongo_client:
            ok, data = mongo_client.dispatch(
                "document_update_one", db_name, collection_name, update_query_kwargs, update_new_kwargs
            )

        return Response(data, exception=not ok)

    @swagger_auto_schema(method="PUT", operation_summary="document_update_many", request_body=DocumentUpdateSerializer)
    @action(detail=True, methods=["PUT"])
    def document_update_many(self, request, pk):
        serializer = DocumentUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        db_name = serializer.data["db_name"]
        collection_name = serializer.data["collection_name"]
        update_query_kwargs = serializer.data["update_query_kwargs"]
        update_new_kwargs = serializer.data["update_new_kwargs"]
        with DbsMongoClient(instance_id=pk) as mongo_client:
            ok, data = mongo_client.dispatch(
                "document_update_many", db_name, collection_name, update_query_kwargs, update_new_kwargs
            )

        return Response(data, exception=not ok)
