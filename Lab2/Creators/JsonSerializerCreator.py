from Creators.SerializerCreator import Creator
from Serializers.Serializer import Serializer
from Serializers.JsonSerialization import JsonSerializer


class JsonSerializerCreator(Creator):
    def create_serializer(self) -> Serializer:
        return JsonSerializer()
