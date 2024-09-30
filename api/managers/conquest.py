from django.db import models


class ConquestManager(models.Manager):
    @staticmethod
    def save(conquests: list):
        for conquest in conquests:
            conquest.save()
            saved_conquests.append(conquest)

        print("--- conquests in ConquestManager ---")
        print(conquests)

        return conquests

    def create(self, **kwargs):
        conquest = self.model(**kwargs)
        conquest.save()
        return conquest

    def update(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass
