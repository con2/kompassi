from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=31)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def name_and_year(self):
        return u"{name} ({year})".format(
            name=self.name,
            year=self.start_time.year
        )
