from django.db import models


class Payment(models.Model):
    """
    Legacy payment, not used by v2 api
    """

    event = models.ForeignKey("core.Event", on_delete=models.CASCADE)

    VERSION = models.CharField(max_length=4)
    STAMP = models.CharField(max_length=20)
    REFERENCE = models.CharField(max_length=20)
    PAYMENT = models.CharField(max_length=20)
    STATUS = models.IntegerField()
    ALGORITHM = models.IntegerField()
    MAC = models.CharField(max_length=32)
