from djongo import models


class MongoModel(models.Model):
    class Meta:
        db_table = 'items'

    _id = models.ObjectIdField()
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
