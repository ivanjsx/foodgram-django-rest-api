from django.db.models import DateTimeField, Model


class WithTimestamps(Model):
    created = DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name="date & time of instance creation",
    )
    modified = DateTimeField(
        auto_now=True,
        verbose_name="date & time of last instance modification",
    )

    class Meta:
        abstract = True
