from django.conf import settings
from django.db import models
import md5

# Create your models here.
class Payment(models.Model):
    test = models.IntegerField(blank=True, null=True)
    VERSION = models.CharField(max_length=4)
    STAMP = models.CharField(max_length=20)
    REFERENCE = models.CharField(max_length=20)
    PAYMENT = models.CharField(max_length=20)
    STATUS = models.IntegerField()
    ALGORITHM = models.IntegerField()
    MAC = models.CharField(max_length=32)

    def _check_mac(self):
    	computed_mac = md5.new()
    	computed_mac.update(settings.CHECKOUT_PARAMS['PASSWORD'])
        computed_mac.update("&")
    	computed_mac.update(self.VERSION)
        computed_mac.update("&")
    	computed_mac.update(self.STAMP)
        computed_mac.update("&")
    	computed_mac.update(self.REFERENCE)
        computed_mac.update("&")
    	computed_mac.update(self.PAYMENT)
        computed_mac.update("&")
    	computed_mac.update(str(self.STATUS))
        computed_mac.update("&")
    	computed_mac.update(str(self.ALGORITHM))

    	return self.MAC != computed_mac.hexdigest().upper

    def clean(self):
        if not self._check_mac():
            from django.core.exceptions import ValidationError
            raise ValidationError('MAC does not match')