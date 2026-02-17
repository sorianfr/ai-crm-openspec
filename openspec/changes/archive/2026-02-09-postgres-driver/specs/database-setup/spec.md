## MODIFIED Requirements

### Requirement: Database connectivity (SQLite and PostgreSQL)

The system SHALL provide database connectivity using SQLAlchemy ORM. It SHALL support SQLite and PostgreSQL backends. The backend SHALL be determined by DATABASE_URL: when the URL is a SQLite URL (e.g. sqlite:///...), the application SHALL use SQLite; when the URL is a PostgreSQL URL (e.g. postgresql+psycopg://...), the application SHALL use the installed PostgreSQL driver (psycopg v3) to connect. SQLite-specific behavior (e.g. connect_args, foreign key pragma) SHALL apply only when using SQLite.

#### Scenario: Database connection module
- **WHEN** the application initializes
- **THEN** database modules SHALL exist at `app/db/session.py` and `app/db/base.py`
- **AND** they SHALL provide database connection configuration

#### Scenario: SQLAlchemy session management
- **WHEN** database operations are performed
- **THEN** SQLAlchemy session factory SHALL be configured
- **AND** dependency injection SHALL provide database sessions to route handlers

#### Scenario: SQLite backend
- **WHEN** DATABASE_URL is a SQLite URL (e.g. sqlite:///./app.db)
- **THEN** the application SHALL connect using SQLite
- **AND** SQLite-specific options (e.g. check_same_thread, foreign_keys) SHALL be applied as needed

#### Scenario: PostgreSQL backend
- **WHEN** DATABASE_URL is a PostgreSQL URL (e.g. postgresql+psycopg://user:pass@host:5432/dbname)
- **THEN** the application SHALL connect using the installed PostgreSQL driver (psycopg v3)
- **AND** the application SHALL operate correctly with PostgreSQL (sessions, migrations, queries)

#### Scenario: Database file creation (SQLite)
- **WHEN** a SQLite database connection is first opened
- **THEN** a SQLite database file SHALL be created at the configured path if it does not exist
- **AND** the database path SHALL be configurable via environment variables

#### Scenario: Database creation via migrations
- **WHEN** Alembic migrations are applied
- **THEN** if the database or schema does not exist, it SHALL be created or updated as per the migration
- **AND** migrations SHALL be applied to the database specified by DATABASE_URL (SQLite or PostgreSQL)

#### Scenario: Database connection lifecycle
- **WHEN** a database session is requested
- **THEN** a new session SHALL be created
- **AND** when the request completes, the session SHALL be properly closed
