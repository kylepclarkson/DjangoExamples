from django.db import models
from django.core.exceptions import ObjectDoesNotExist

"""
A custom class for ordering objects by fields. 
"""
class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        # Override
        if getattr(model_instance, self.attname) is None:
            try:
                # Value already exists for this field in the model.
                querySet = self.model.objects.all()
                if self.for_fields:
                    # Filter by objects with the same field values as specified in "for_fields"
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    querySet = querySet.filter(**query)

                # the object with the highest order
                last_item = querySet.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                # Value does not exist.
                value = 0

            # Assign the order to the field's value in the model.
            setattr(model_instance, self.attname, value)
            return value
        
        else:
            return super(OrderField, self).pre_save(model_instance, add)
                

                