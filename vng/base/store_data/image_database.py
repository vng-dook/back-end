from base.models import TargetImage
from django.contrib.gis.geos import Point
from django.core.files import File
from uuid import uuid4


def store_image(lng, lat, img_name, title, user_instance):
    image_id = uuid4()
    targetImage = TargetImage(user=user_instance)
    targetImage.image_id = image_id
    targetImage.image = File(file=open(img_name, 'rb'), name=img_name)
    targetImage.title = title
    targetImage.image_name = img_name
    try:
        point_image = Point(lng, lat)
        targetImage.geom = point_image
    except TypeError:
        return TypeError
    targetImage.save()
    return image_id
