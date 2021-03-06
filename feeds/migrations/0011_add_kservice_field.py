# Generated by Django 3.0.7 on 2020-08-24 08:46

from django.db import migrations, models
import feeds.models.tag


class Migration(migrations.Migration):

    replaces = [('feeds', '0011_auto_20200816_0633'), ('feeds', '0012_auto_20200824_0844')]

    dependencies = [
        ('feeds', '0010_website_category_and_defaults'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Short descriptive name for this category.', max_length=200),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(help_text='Short descriptive unique name for use in urls.', max_length=255),
        ),
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
