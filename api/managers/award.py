from django.db import models


class AwardManager(models.Manager):
    def save(self, awards):
        return self.bulk_create(awards)

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass
