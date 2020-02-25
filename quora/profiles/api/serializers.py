from rest_framework import serializers

from profiles.models import Profile


class ProfileDisplaySerializer(serializers.ModelSerializer):
    """
    A serializer used to fetch info of a current user
    """

    class Meta:
        model = Profile
        fields = ('username', )

