# Generated by Django 2.1.7 on 2019-04-02 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breakdown', '0004_auto_20190401_2202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('course', models.CharField(max_length=30)),
                ('opened', models.BooleanField()),
                ('created', models.DateTimeField()),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField()),
                ('add_info', models.TextField()),
                ('form_factor', models.CharField(max_length=30)),
                ('min_people', models.IntegerField()),
                ('max_people', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Survey',
                'verbose_name_plural': 'Surveys',
            },
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]