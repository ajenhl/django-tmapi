# -*- coding: utf-8 -*-


from django.db import models, migrations
import tmapi.models.locator
import tmapi.models.construct


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            bases=(tmapi.models.construct.Construct, models.Model),
        ),
        migrations.CreateModel(
            name='Identifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemIdentifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=512)),
            ],
            bases=(tmapi.models.locator.LocatorBase, models.Model),
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.TextField()),
                ('identifier', models.OneToOneField(related_name='name', to='tmapi.Identifier')),
                ('item_identifiers', models.ManyToManyField(related_name='name', to='tmapi.ItemIdentifier')),
            ],
            bases=(tmapi.models.construct.Construct, models.Model),
        ),
        migrations.CreateModel(
            name='Occurrence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datatype', models.CharField(max_length=512, blank=True)),
                ('value', models.TextField()),
                ('identifier', models.OneToOneField(related_name='occurrence', to='tmapi.Identifier')),
                ('item_identifiers', models.ManyToManyField(related_name='occurrence', to='tmapi.ItemIdentifier')),
            ],
            bases=(tmapi.models.construct.Construct, models.Model),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('association', models.ForeignKey(related_name='roles', to='tmapi.Association')),
                ('identifier', models.OneToOneField(related_name='role', to='tmapi.Identifier')),
                ('item_identifiers', models.ManyToManyField(related_name='role', to='tmapi.ItemIdentifier')),
            ],
            bases=(tmapi.models.construct.Construct, models.Model),
        ),
        migrations.CreateModel(
            name='SubjectIdentifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=512, db_index=True)),
            ],
            bases=(tmapi.models.locator.LocatorBase, models.Model),
        ),
        migrations.CreateModel(
            name='SubjectLocator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=512)),
            ],
            bases=(tmapi.models.locator.LocatorBase, models.Model),
        ),
        migrations.CreateModel(
            name='TMAPIFeature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feature_string', models.CharField(max_length=512)),
                ('value', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.OneToOneField(related_name='topic', to='tmapi.Identifier')),
                ('item_identifiers', models.ManyToManyField(related_name='topic', to='tmapi.ItemIdentifier')),
            ],
            bases=(tmapi.models.construct.Construct, models.Model),
        ),
        migrations.CreateModel(
            name='TopicMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iri', models.CharField(max_length=512)),
                ('title', models.CharField(max_length=128, blank=True)),
                ('base_address', models.CharField(max_length=512, blank=True)),
                ('identifier', models.OneToOneField(related_name='topicmap', to='tmapi.Identifier')),
                ('item_identifiers', models.ManyToManyField(related_name='topicmap', to='tmapi.ItemIdentifier')),
                ('reifier', models.OneToOneField(related_name='reified_topicmap', null=True, to='tmapi.Topic')),
            ],
            bases=(tmapi.models.construct.Construct, models.Model),
        ),
        migrations.CreateModel(
            name='TopicMapSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datatype', models.CharField(max_length=512, blank=True)),
                ('value', models.TextField()),
                ('identifier', models.OneToOneField(related_name='variant', to='tmapi.Identifier')),
                ('item_identifiers', models.ManyToManyField(related_name='variant', to='tmapi.ItemIdentifier')),
                ('name', models.ForeignKey(related_name='variants', to='tmapi.Name')),
                ('reifier', models.OneToOneField(related_name='reified_variant', null=True, to='tmapi.Topic')),
                ('scope', models.ManyToManyField(related_name='scoped_variants', to='tmapi.Topic')),
                ('topic_map', models.ForeignKey(related_name='variant_constructs', to='tmapi.TopicMap')),
            ],
            bases=(tmapi.models.construct.Construct, models.Model),
        ),
        migrations.AddField(
            model_name='topicmap',
            name='topic_map_system',
            field=models.ForeignKey(related_name='topic_maps', to='tmapi.TopicMapSystem'),
        ),
        migrations.AddField(
            model_name='topic',
            name='topic_map',
            field=models.ForeignKey(related_name='topic_constructs', to='tmapi.TopicMap'),
        ),
        migrations.AddField(
            model_name='topic',
            name='types',
            field=models.ManyToManyField(related_name='typed_topics', to='tmapi.Topic', blank=True),
        ),
        migrations.AddField(
            model_name='tmapifeature',
            name='topic_map_system',
            field=models.ForeignKey(related_name='features', to='tmapi.TopicMapSystem'),
        ),
        migrations.AddField(
            model_name='subjectlocator',
            name='containing_topic_map',
            field=models.ForeignKey(related_name='subject_locators_in_map', to='tmapi.TopicMap'),
        ),
        migrations.AddField(
            model_name='subjectlocator',
            name='topic',
            field=models.ForeignKey(related_name='subject_locators', to='tmapi.Topic'),
        ),
        migrations.AddField(
            model_name='subjectidentifier',
            name='containing_topic_map',
            field=models.ForeignKey(related_name='subject_identifiers_in_map', to='tmapi.TopicMap'),
        ),
        migrations.AddField(
            model_name='subjectidentifier',
            name='topic',
            field=models.ForeignKey(related_name='subject_identifiers', to='tmapi.Topic'),
        ),
        migrations.AddField(
            model_name='role',
            name='player',
            field=models.ForeignKey(related_name='roles', to='tmapi.Topic'),
        ),
        migrations.AddField(
            model_name='role',
            name='reifier',
            field=models.OneToOneField(related_name='reified_role', null=True, to='tmapi.Topic'),
        ),
        migrations.AddField(
            model_name='role',
            name='topic_map',
            field=models.ForeignKey(related_name='role_constructs', to='tmapi.TopicMap'),
        ),
        migrations.AddField(
            model_name='role',
            name='type',
            field=models.ForeignKey(related_name='typed_roles', to='tmapi.Topic'),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='reifier',
            field=models.OneToOneField(related_name='reified_occurrence', null=True, to='tmapi.Topic'),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='scope',
            field=models.ManyToManyField(related_name='scoped_occurrences', to='tmapi.Topic'),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='topic',
            field=models.ForeignKey(related_name='occurrences', to='tmapi.Topic'),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='topic_map',
            field=models.ForeignKey(related_name='occurrence_constructs', to='tmapi.TopicMap'),
        ),
        migrations.AddField(
            model_name='occurrence',
            name='type',
            field=models.ForeignKey(related_name='typed_occurrences', to='tmapi.Topic'),
        ),
        migrations.AddField(
            model_name='name',
            name='reifier',
            field=models.OneToOneField(related_name='reified_name', null=True, to='tmapi.Topic'),
        ),
        migrations.AddField(
            model_name='name',
            name='scope',
            field=models.ManyToManyField(related_name='scoped_names', to='tmapi.Topic'),
        ),
        migrations.AddField(
            model_name='name',
            name='topic',
            field=models.ForeignKey(related_name='names', to='tmapi.Topic'),
        ),
        migrations.AddField(
            model_name='name',
            name='topic_map',
            field=models.ForeignKey(related_name='name_constructs', to='tmapi.TopicMap'),
        ),
        migrations.AddField(
            model_name='name',
            name='type',
            field=models.ForeignKey(related_name='typed_names', to='tmapi.Topic'),
        ),
        migrations.AddField(
            model_name='itemidentifier',
            name='containing_topic_map',
            field=models.ForeignKey(related_name='item_identifiers_in_map', to='tmapi.TopicMap'),
        ),
        migrations.AddField(
            model_name='identifier',
            name='containing_topic_map',
            field=models.ForeignKey(related_name='identifiers_in_map', to='tmapi.TopicMap', null=True),
        ),
        migrations.AddField(
            model_name='association',
            name='identifier',
            field=models.OneToOneField(related_name='association', to='tmapi.Identifier'),
        ),
        migrations.AddField(
            model_name='association',
            name='item_identifiers',
            field=models.ManyToManyField(related_name='association', to='tmapi.ItemIdentifier'),
        ),
        migrations.AddField(
            model_name='association',
            name='reifier',
            field=models.OneToOneField(related_name='reified_association', null=True, to='tmapi.Topic'),
        ),
        migrations.AddField(
            model_name='association',
            name='scope',
            field=models.ManyToManyField(related_name='scoped_associations', to='tmapi.Topic'),
        ),
        migrations.AddField(
            model_name='association',
            name='topic_map',
            field=models.ForeignKey(related_name='association_constructs', to='tmapi.TopicMap'),
        ),
        migrations.AddField(
            model_name='association',
            name='type',
            field=models.ForeignKey(related_name='typed_associations', to='tmapi.Topic'),
        ),
        migrations.AlterUniqueTogether(
            name='tmapifeature',
            unique_together=set([('topic_map_system', 'feature_string')]),
        ),
        migrations.AlterUniqueTogether(
            name='itemidentifier',
            unique_together=set([('address', 'containing_topic_map')]),
        ),
    ]
