# Generated by Django 4.1 on 2022-08-23 07:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "rentings",
            "0002_alter_through_event_user_customer_obj_user_customer_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="room",
            name="user",
        ),
        migrations.AddField(
            model_name="event",
            name="obj_user_busines",
            field=models.ForeignKey(
                limit_choices_to={"groups": 2},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Event",
                to=settings.AUTH_USER_MODEL,
                verbose_name="User_busines",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="obj_room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="Events",
                to="rentings.room",
                verbose_name="Rooms",
            ),
        ),
        migrations.AlterField(
            model_name="through_event_user_customer",
            name="obj_user_customer",
            field=models.ForeignKey(
                limit_choices_to={"groups": 1},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="Through_Event_User_customer",
                to=settings.AUTH_USER_MODEL,
                verbose_name="User_customer",
            ),
        ),
        migrations.DeleteModel(
            name="Through_Room_User_busines",
        ),
    ]
