# Generated by Django 2.2.2 on 2019-06-19 05:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('justnow_app', '0002_auto_20190618_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='answers', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]