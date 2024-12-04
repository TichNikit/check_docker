from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

from database import Base  # Импортируйте ваши модели
from database import Film_historic, Film_horror, Film_thriller

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for logging
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Add your model's MetaData object here
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    connectable = engine_from_config(
        configuration,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

# This line will determine which migration mode to use.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()