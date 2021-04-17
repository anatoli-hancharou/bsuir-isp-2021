from Creators.SerializerCreator import Creator
from Serializers.Serializer import Serializer
from Serializers.PickleSerialization import PickleSerializer


class PickleSerializerCreator(Creator):
    def create_serializer(self) -> Serializer:
        return PickleSerializer()
