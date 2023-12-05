# Generated by Django 3.2 on 2023-12-05 14:31

import colorfield.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='date & time of instance creation')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date & time of last instance modification')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='date & time of instance creation')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date & time of last instance modification')),
                ('title', models.CharField(help_text='Provide a title', max_length=256, verbose_name='title')),
                ('measurement_unit', models.CharField(help_text='Provide a measurement unit', max_length=20, verbose_name='measurement unit')),
            ],
            options={
                'ordering': ('title',),
                'abstract': False,
                'default_related_name': 'ingredients',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='date & time of instance creation')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date & time of last instance modification')),
                ('title', models.CharField(help_text='Provide a title', max_length=256, verbose_name='title')),
                ('description', models.TextField(help_text='Provide a description', verbose_name='description')),
                ('cooking_time', models.PositiveSmallIntegerField(help_text='Provide a cooking, in minutes', verbose_name='Cooking time, in minutes')),
                ('cover_image', models.ImageField(help_text='Upload a cover image', upload_to='recipes/', verbose_name='Cover image')),
            ],
            options={
                'ordering': ('-created',),
                'abstract': False,
                'default_related_name': 'recipes',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='date & time of instance creation')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date & time of last instance modification')),
                ('quantity', models.FloatField(help_text='Provide a quantity needed', verbose_name='quantity')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='date & time of instance creation')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date & time of last instance modification')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='date & time of instance creation')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date & time of last instance modification')),
                ('title', models.CharField(help_text='Provide a title', max_length=256, verbose_name='title')),
                ('slug', models.SlugField(help_text='Provide a unique slug (will be used in the URL address)', unique=True, verbose_name='slug')),
                ('hex_color', colorfield.fields.ColorField(default='#FF0000', help_text='Provide a unique color', image_field=None, max_length=25, samples=None, unique=True, verbose_name='color')),
            ],
            options={
                'ordering': ('title',),
                'abstract': False,
                'default_related_name': 'tags',
            },
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(fields=('title',), name='tag title must be unique'),
        ),
        migrations.AddField(
            model_name='recipetag',
            name='recipe',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe'),
        ),
        migrations.AddField(
            model_name='recipetag',
            name='tag',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='recipes.tag'),
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient'),
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(help_text='Provide a set of ingredients it includes', related_name='recipes', through='recipes.RecipeIngredient', to='recipes.Ingredient', verbose_name='Set of ingredients'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(blank=True, help_text='Provide a set of tags it belongs to', related_name='recipes', through='recipes.RecipeTag', to='recipes.Tag', verbose_name='Set of tags'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('title', 'measurement_unit'), name='title & measurement_unit must make a unique pair'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='recipetag',
            constraint=models.UniqueConstraint(fields=('recipe', 'tag'), name='recipe & tag must make a unique pair'),
        ),
        migrations.AddConstraint(
            model_name='recipeingredient',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='recipe & ingredient must make a unique pair'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='user & recipe must make a unique pair'),
        ),
    ]
