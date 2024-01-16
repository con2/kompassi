from django.db import models


class ScheduleItem(models.Model):
    program = models.ForeignKey("program_v2.Program", on_delete=models.CASCADE, related_name="schedule_items")
    subtitle = models.CharField(max_length=255, blank=True)
    start_time = models.DateTimeField()
    length = models.DurationField()

    def __str__(self):
        return self.title

    @property
    def title(self):
        if self.subtitle:
            return f"{self.program.title}: {self.subtitle}"
        else:
            return self.program.title

    @property
    def end_time(self):
        return self.start_time + self.length
