# Generated by Django 4.2.5 on 2025-03-04 22:08

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('ine', models.CharField(max_length=25)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telephone', models.CharField(max_length=15, unique=True)),
                ('genre', models.CharField(max_length=50)),
                ('filiere', models.CharField(max_length=255)),
                ('niveau_etude', models.CharField(max_length=50)),
                ('can_continue', models.BooleanField(default=True)),
                ('date_inscription', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Seance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_debut', models.DateTimeField(auto_now_add=True)),
                ('date_fin', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Presence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presence', models.BooleanField(default=False)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suiviPresence.participant')),
                ('seance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suiviPresence.seance')),
            ],
        ),
        migrations.CreateModel(
            name='Groupe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, unique=True)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suiviPresence.participant')),
            ],
        ),
    ]
