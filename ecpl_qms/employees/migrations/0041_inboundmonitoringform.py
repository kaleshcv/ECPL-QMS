# Generated by Django 3.1.3 on 2020-12-10 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0040_auto_20201210_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='InboundMonitoringForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.IntegerField()),
                ('associate_name', models.CharField(max_length=50)),
                ('qa', models.CharField(max_length=50)),
                ('team_lead', models.CharField(max_length=50)),
                ('customer_name', models.CharField(max_length=50)),
                ('customer_contact', models.IntegerField()),
                ('call_date', models.DateField()),
                ('audit_date', models.DateField()),
                ('campaign', models.CharField(max_length=100)),
                ('zone', models.CharField(max_length=50)),
                ('concept', models.CharField(max_length=60)),
                ('call_duration', models.IntegerField()),
                ('ce_1', models.IntegerField()),
                ('ce_2', models.IntegerField()),
                ('ce_3', models.IntegerField()),
                ('ce_4', models.IntegerField()),
                ('ce_5', models.IntegerField()),
                ('ce_6', models.IntegerField()),
                ('ce_7', models.IntegerField()),
                ('ce_8', models.IntegerField()),
                ('ce_9', models.IntegerField()),
                ('ce_10', models.IntegerField()),
                ('ce_11', models.IntegerField()),
                ('business_1', models.IntegerField()),
                ('compliance_1', models.IntegerField()),
                ('compliance_2', models.IntegerField()),
                ('compliance_3', models.IntegerField()),
                ('areas_improvement', models.TextField()),
                ('positives', models.TextField()),
                ('comments', models.TextField()),
                ('added_by', models.CharField(max_length=30)),
                ('status', models.BooleanField(default=False)),
                ('closed_date', models.DateTimeField(null=True)),
                ('emp_comments', models.TextField(null=True)),
                ('ce_total', models.IntegerField(null=True)),
                ('business_total', models.IntegerField(null=True)),
                ('compliance_total', models.IntegerField(null=True)),
                ('overall_score', models.IntegerField(null=True)),
            ],
        ),
    ]
