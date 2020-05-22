# Generated by Django 2.2.5 on 2019-09-16 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('social_networks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(choices=[('en', 'English'), ('ru', 'Russian')], default='en', max_length=7, verbose_name='Язык')),
                ('slug', models.SlugField(blank=True, help_text='Укажите url', max_length=500, null=True, verbose_name='url')),
                ('name', models.CharField(default='Контакты', max_length=100, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=5000, null=True, verbose_name='Описание')),
                ('map', models.CharField(blank=True, max_length=10000, null=True, verbose_name='Карта')),
            ],
            options={
                'verbose_name': 'Контакт',
                'verbose_name_plural': 'Контакты',
                'unique_together': {('lang', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='ФИО')),
                ('email', models.EmailField(max_length=150, verbose_name='Почта')),
                ('phone', models.CharField(max_length=14, verbose_name='Телефон')),
                ('subject', models.CharField(max_length=150, verbose_name='Тема')),
                ('message', models.TextField(max_length=1000, verbose_name='Сообщение')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'Обратная связь',
                'verbose_name_plural': 'Обратные связи',
            },
        ),
        migrations.CreateModel(
            name='ContactSocNet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('your_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ваша ссылка')),
                ('contact_soc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='soc_net', to='contact.Contact', verbose_name='Контакт')),
                ('link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='social_networks.SocialNetworks', verbose_name='Соц. сеть')),
            ],
            options={
                'verbose_name': 'Соц. сеть',
                'verbose_name_plural': 'Соц. сети',
            },
        ),
        migrations.CreateModel(
            name='ContactFields',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=1000, verbose_name='Поле 1')),
                ('text_two', models.CharField(blank=True, max_length=1000, verbose_name='Поле 2')),
                ('icon_ui', models.CharField(blank=True, max_length=500, verbose_name='Класс иконки')),
                ('icon', models.FileField(blank=True, null=True, upload_to='icon/', verbose_name='Иконка')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_field', to='contact.Contact', verbose_name='Контакты')),
            ],
            options={
                'verbose_name': 'Поле контактов',
                'verbose_name_plural': 'Поля контактов',
                'ordering': ['id'],
            },
        ),
    ]