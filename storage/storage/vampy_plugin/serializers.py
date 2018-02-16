from rest_framework import serializers

from storage.vampy_plugin.models import VampyPluginOutput, VampyPluginCategory, VampyPlugin


class VampyPluginOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = VampyPluginOutput
        fields = ('name')


class VampyPluginCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VampyPluginCategory
        fields = ('name')


class VampyPluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = VampyPlugin
        fields = ('provider', 'name')
