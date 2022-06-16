from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("user_interaction", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER vector_column_trigger_job
            BEFORE INSERT OR UPDATE OF title, description
            ON user_interaction_job
            FOR EACH ROW EXECUTE PROCEDURE
            tsvector_update_trigger(
                vector_column, 'pg_catalog.english', title, description
            );
            CREATE TRIGGER vector_column_trigger_student
            BEFORE INSERT OR UPDATE OF profile
            ON user_interaction_student
            FOR EACH ROW EXECUTE PROCEDURE
            tsvector_update_trigger(
                vector_column, 'pg_catalog.english', profile
            );
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS vector_column_trigger_job
            ON user_interaction_job;
            DROP TRIGGER IF EXISTS vector_column_trigger_student
            ON user_interaction_student;
            """,
        ),
    ]
