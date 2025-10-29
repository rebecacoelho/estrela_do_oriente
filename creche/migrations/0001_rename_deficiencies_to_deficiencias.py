# Generated migration to fix typo in field name

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(
            # Renomeia a coluna no banco de dados
            sql='ALTER TABLE creche_aluno RENAME COLUMN deficiencies_multiplas TO deficiencias_multiplas;',
            # SQL para reverter (caso necessário)
            reverse_sql='ALTER TABLE creche_aluno RENAME COLUMN deficiencias_multiplas TO deficiencies_multiplas;',
        ),
    ]

