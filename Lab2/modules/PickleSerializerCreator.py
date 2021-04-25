from modules.SerializerCreator import Creator
from modules.Serializer import Serializer
from modules.PickleSerialization import PickleSerializer


class PickleSerializerCreator(Creator):
    def create_serializer(self) -> Serializer:
        return PickleSerializer()
