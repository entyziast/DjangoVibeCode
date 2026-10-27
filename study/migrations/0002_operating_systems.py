from django.db import migrations


def create_subject(apps, schema_editor):
    Subject = apps.get_model("study", "Subject")
    Subject.objects.using(schema_editor.connection.alias).get_or_create(
        slug="operating-systems",
        defaults={"name": "Операционные системы"},
    )


class Migration(migrations.Migration):
    dependencies = [("study", "0001_initial")]

    operations = [
        migrations.RunPython(create_subject, reverse_code=migrations.RunPython.noop),
    ]
