alembic revision --autogenerate -m "Added new column to users"
alembic upgrade head
pip install alembic
