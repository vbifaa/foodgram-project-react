from recipes.models import Tag, Ingredient


def create_objects(creator, objects):
    for id in range(len(objects)):
        creator(objects[id])
        objects[id]['id'] = id + 1
    return objects

def tag_creator(object):
    Tag.objects.create(
        name=object['name'],
        color=object['color'],
        slug=object['slug']
    )

def ingredient_creator(object):
    Ingredient.objects.create(
        name=object['name'],
        measurement_unit=object['measurement_unit']
    )
