from django.db import models as django_models


class EventManager(django_models.Manager):
    @staticmethod
    def save(instance):
        instance.save()
        return instance

    @staticmethod
    def set_related_entities(event, related_entities):
        event.activity_set = related_entities['activities']
        event.conquest_set = related_entities['conquests']
        event.stamp_set = related_entities['stamps']
        event.award_set = related_entities['awards']

        return event

    @staticmethod
    def update(instance, **kwargs):
        instance.name = kwargs['name']
        instance.year = kwargs['year']
        instance.edition_number = kwargs['edition_number']

        instance.save()

    @staticmethod
    def delete(instance):
        instance.delete()

    @staticmethod
    def get_all_from(user, should_get_created_events: bool):
        if should_get_created_events:
            return user.events_created.all()
        else:
            return user.events_participating.all()
