# Generated by Django 3.1.3 on 2020-11-09 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='coaching',
            name='qa',
            field=models.CharField(default='test', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coaching',
            name='ticket_no',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='coaching',
            name='agent',
            field=models.CharField(max_length=50),
        ),
    ]
