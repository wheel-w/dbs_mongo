from rest_framework.routers import DefaultRouter

from manager.views.mongo_instance import MongoInstanceViewSet

router = DefaultRouter()
router.register("mongo/instance", MongoInstanceViewSet, basename="mongo_instance")

urlpatterns = router.urls
