import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Importa tutti i metadata dei moduli (aggiungine quanti vuoi)
from app.paperless import models as paperless_models

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 🔥 Prendi lo schema da variabile d'ambiente
TARGET_SCHEMA = os.getenv("ALEMBIC_SCHEMA", "public")

# Se usi più moduli, potresti voler creare un mapping schema -> metadata
SCHEMA_METADATA = {
    "paperless": paperless_models.Base.metadata,
    "public": paperless_models.Base.metadata,  # fallback (oppure niente)
}

target_metadata = SCHEMA_METADATA.get(TARGET_SCHEMA)

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        version_table_schema=TARGET_SCHEMA,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            version_table_schema=TARGET_SCHEMA,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
