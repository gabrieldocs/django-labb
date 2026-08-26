from django.urls import path, include
from .models import Schedule
from rest_framework import routers, serializers, viewsets, permissions
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ["id", "username", "email"]

    
class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Schedule
        fields = ["title", "user", "description", "created_at"]


class ScheduleViewset(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().select_related("user")
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
router = routers.DefaultRouter()
router.register(r"schedules", ScheduleViewset)

urlpatterns = [
    path("", include(router.urls)),
]