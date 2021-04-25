from modules.SerializerCreator import Creator
from modules.Serializer import Serializer
from modules.JsonSerialization import JsonSerializer


class JsonSerializerCreator(Creator):
    def create_serializer(self) -> Serializer:
        return JsonSerializer()
