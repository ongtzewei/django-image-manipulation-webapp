import base64
from io import BytesIO
from PIL import Image as PILImage
from drf_extra_fields.fields import Base64ImageField
from api.utils import retrieve_remote_image


class Base64ImageField(Base64ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str):
            # link to remote image is provided
            data = retrieve_remote_image(data)
        else:
            # file is uploaded or is existing image from system
            buffer = BytesIO()
            image = isinstance(data, PILImage.Image) and data or PILImage.open(data)
            image.save(buffer, format='png')
            data = "data:image/png;base64,"+base64.b64encode(buffer.getvalue()).decode()
        return super(Base64ImageField, self).to_internal_value(data)
