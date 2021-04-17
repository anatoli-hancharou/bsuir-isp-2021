from Creators.SerializerCreator import Creator
from Serializers.Serializer import Serializer
from Serializers.TomlSerialization import TomlSerializer


class TomlSerializerCreator(Creator):
    def create_serializer(self) -> Serializer:
        return TomlSerializer()
