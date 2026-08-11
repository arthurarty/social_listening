from sqlmodel import SQLModel

# Deterministic naming convention for constraints/indexes so Alembic
# autogenerate always emits real constraint names (e.g. "fk_tweets_category_categories")
# instead of leaving them unnamed, which left the downgrade in
# b4adc78485bc_add_categories_table.py unable to reference the foreign key it created.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
SQLModel.metadata.naming_convention = NAMING_CONVENTION
