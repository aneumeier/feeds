# Generated by Django 3.0.7 on 2020-08-24 08:44

from django.db import migrations, models
import feeds.models.tag


class Migration(migrations.Migration):

    dependencies = [
        ('feeds', '0011_auto_20200816_0633'),
    ]

    operations = [
        migrations.AddField(
            model_name='feed',
            name='last_k_checked',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='last checked by kubernetes service'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=feeds.models.tag.TagNameField(db_index=True, max_length=50, unique=True, verbose_name='name'),
        ),
    ]