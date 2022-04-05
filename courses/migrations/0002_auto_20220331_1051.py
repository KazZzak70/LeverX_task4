from django.db import migrations


def combine_course_names(apps, schema_editor):
    Course = apps.get_model("courses", "Course")
    for course in Course.objects.all():
        course.name = f"{course.name}_{course.id}"
        course.save()


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(combine_course_names)
    ]
