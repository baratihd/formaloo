from rest_framework import serializers

from apps.store.models import App


__all__ = ('AppSerializer',)


class AppSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = App
        fields = ('id', 'title', 'description', 'price', 'owner', 'is_verified', 'created_at', 'updated_at')
        read_only_fields = ('id', 'is_verified', 'created_at', 'updated_at')
