from Creators.JsonSerializerCreator import JsonSerializerCreator

serializer = JsonSerializerCreator().create_serializer()

func = serializer.load('file.json')
func()
