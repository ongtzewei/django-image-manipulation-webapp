import base64
import urllib3
from io import BytesIO
from PIL import Image as PILImage
from drf_extra_fields.fields import Base64ImageField

http = urllib3.PoolManager()

class Base64ImageField(Base64ImageField):
  
  def to_internal_value(self, data):
    buffer = BytesIO()
    if isinstance(data, str):
      response = http.request('GET', data)
      image = PILImage.open(BytesIO(response.data))
    else:
      image = isinstance(data, PILImage.Image) and data or PILImage.open(data)
    image.save(buffer, format='png')
    data = "data:image/png;base64,"+base64.b64encode(buffer.getvalue()).decode()
    return super(Base64ImageField, self).to_internal_value(data)