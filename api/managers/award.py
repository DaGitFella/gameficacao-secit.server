from django.db import models


class AwardManager(models.Manager):
    @staticmethod
    def save(awards):
        for award in awards:
            award.save()

        return awards

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass
