DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'deposito') THEN
        CREATE DATABASE deposito;
    END IF;
END$$;