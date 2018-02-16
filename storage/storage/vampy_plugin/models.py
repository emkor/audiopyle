from django.db import models


class VampyPluginCategory(models.Model):
    name = models.CharField(blank=False, null=False, db_index=True, unique=True, max_length=100)


class VampyPlugin(models.Model):
    provider = models.CharField(blank=False, null=False, db_index=True, max_length=100)
    name = models.CharField(blank=False, null=False, db_index=True, max_length=100)
    categories = models.ManyToManyField(VampyPluginCategory)

    class Meta:
        unique_together = (('provider', 'name'),)


class VampyPluginOutput(models.Model):
    plugin = models.ForeignKey(VampyPlugin, on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, db_index=True, unique=True, max_length=100)
