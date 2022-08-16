# Generated by Django 4.0.5 on 2022-06-28 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('final_app', '0011_comment_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='name',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='post',
        ),
        migrations.AddField(
            model_name='comment',
            name='message_id',
            field=models.ForeignKey( on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='final_app.articles'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user_id',
            field=models.ForeignKey( on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='final_app.users'),
        ),
    ]
