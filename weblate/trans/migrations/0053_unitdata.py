# Generated by Django 2.2.5 on 2019-12-12 14:12

from django.db import migrations

MODELS = [("trans", "Comment"), ("trans", "Suggestion"), ("checks", "Check")]


def migrate_unitdata(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    Unit = apps.get_model("trans", "Unit")

    for model in (apps.get_model(*args) for args in MODELS):
        # Create new objects for each related unit
        for obj in model.objects.using(db_alias).filter(unit=None).iterator():
            units = Unit.objects.using(db_alias).filter(
                content_hash=obj.content_hash,
                translation__component__project=obj.project,
            )
            if obj.language is None:
                units = units.filter(translation__language=obj.project.source_language)
            else:
                units = units.filter(translation__language=obj.language)
            # Using __getstate__ would be cleaner, but needs Django 2.0
            state = dict(obj.__dict__)
            del state["_state"]
            del state["id"]
            del state["unit_id"]
            for unit in units:
                if model.objects.using(db_alias).filter(unit=unit, **state).exists():
                    continue
                model.objects.using(db_alias).create(unit=unit, **state)

        # Remove old objects without unit link
        model.objects.using(db_alias).filter(unit=None).delete()


class Migration(migrations.Migration):

    dependencies = [("trans", "0052_auto_20191212_1403"), ("checks", "0002_check_unit")]

    operations = [
        migrations.RunPython(migrate_unitdata, migrations.RunPython.noop, elidable=True)
    ]
