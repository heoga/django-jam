from jam.models.profile import Profile
from rest_framework import serializers, viewsets


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('url', 'user', 'theme')


# ViewSets define the view behavior.
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
