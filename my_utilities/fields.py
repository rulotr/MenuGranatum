from django.db import models

class TrimpCharField(models.CharField):
    def to_python(self, value):
        value = super().to_python(value)
        if value is not None:
            value = value.strip()
        return value