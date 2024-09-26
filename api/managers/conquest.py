from django.db import models


class ConquestManager(models.Manager):
    @staticmethod
    def save(conquests):
        return ConquestManager.bulk_create(conquests)

    def create(self, **kwargs):
        conquest = self.model(**kwargs)
        conquest.save()
        return conquest

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass
