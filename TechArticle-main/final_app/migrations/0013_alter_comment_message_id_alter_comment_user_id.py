# Generated by Django 4.0.5 on 2022-06-28 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('final_app', '0012_remove_comment_name_remove_comment_post_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='message_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='final_app.articles'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='final_app.users'),
        ),
    ]
