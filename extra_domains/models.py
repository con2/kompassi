from django.db import models


class ExtraDomain(models.Model):
    domain_name = models.CharField(max_length=63, unique=True)
    root_urlconf = models.CharField(max_length=63)

    @property
    def args(self):
        return list(self.viewarg_set.order_by('order'))

    @property
    def kwargs(self):
        return dict((p.key, p.value) for p in self.viewkwarg_set.all())

    @classmethod
    def get_for_request(cls, request):
        hostname = request.META['HTTP_HOST'].split(':')[0]
        try:
            return cls.objects.get(domain_name=hostname)
        except cls.DoesNotExist:
            return None

    def __unicode__(self):
        return self.domain_name or u'None'


class ViewArg(models.Model):
    extra_domain = models.ForeignKey(ExtraDomain)
    order = models.IntegerField()
    value = models.CharField(max_length=63)


class ViewKwarg(models.Model):
    extra_domain = models.ForeignKey(ExtraDomain)
    key = models.CharField(max_length=63)
    value = models.CharField(max_length=63)