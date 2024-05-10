export APP_ENV=dev;

export POSTGRES_USER=admin;
export POSTGRES_PASSWORD=pass;
export POSTGRES_HOST=127.0.0.1;
export POSTGRES_PORT=5432;
export POSTGRES_DB=book_storage;
export POSTGRES_ENGINE=postgresql;
export POSTGRES_DB_SCHEMA=public;

export RMQ_USER=admin;
export RMQ_PASSWORD=pass;
export RMQ_HOST=127.0.0.1;
export RMQ_PORT=5672;

export RMQ_RUN_SETTINGS='{"queues":{},"bindings":{},"exchanges":{}}';

cd src/kernel/database/postgres;
alembic revision --autogenerate -m "fix TokenModel";
