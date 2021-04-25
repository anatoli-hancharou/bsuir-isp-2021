from modules.SerializerCreator import Creator
from modules.Serializer import Serializer
from modules.YamlSerialization import YamlSerializer


class YamlSerializerCreator(Creator):
    def create_serializer(self) -> Serializer:
        return YamlSerializer()
