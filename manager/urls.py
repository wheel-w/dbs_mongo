from rest_framework.routers import DefaultRouter

from manager.views.mongo_instance import MongoInstanceViewSet
from manager.views.mongo_operation import MongoOperationViewSet

router = DefaultRouter()
router.register("mongo/instance", MongoInstanceViewSet, basename="mongo_instance")
router.register("mongo/operation", MongoOperationViewSet, basename="mongo_instance")

urlpatterns = router.urls
