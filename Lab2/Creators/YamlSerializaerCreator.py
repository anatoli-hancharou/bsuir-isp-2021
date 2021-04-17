from Creators.SerializerCreator import Creator
from Serializers.Serializer import Serializer
from Serializers.YamlSerialization import YamlSerializer


class YamlSerializerCreator(Creator):
    def create_serializer(self) -> Serializer:
        return YamlSerializer()
