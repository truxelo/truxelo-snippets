# Bridge

A user data synchronisation application built with Domain-Driven Design principles, featuring a CLI interface and SQLite persistence layer.

## Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. Clone the repository and navigate to the project directory
2. Install dependencies and set up the development environment:

```bash
make init
```

### Available Commands

The project uses a Makefile for common development tasks:

```bash
make help     # Show all available commands
make init     # Initialize local environment with uv
make format   # Format code with black and isort
make lint     # Run all linters and type checkers
make tests    # Run unit tests with coverage
make build    # Build Python wheel package
```

### Usage

After installation, you can use the CLI tool:

```bash
# Database management
bridge database upgrade    # Apply database migrations
bridge database current    # Show current migration version

# User management
bridge users create --email user@example.com --first-name John --last-name Doe
bridge users list --limit 10 --offset 0
bridge users update user@example.com --first-name Jane
bridge users delete user@example.com
```

## Project Architecture

This project follows **Domain-Driven Design (DDD)** principles with a clean layered architecture:

```
src/bridge/
├── cli/           # Application/CLI Layer
├── domain/        # Domain Layer (Core Business Logic)
├── database/      # Infrastructure/Persistence Layer
└── config.py      # Configuration
```

### Layer Dependencies

The architecture enforces strict dependency rules:

- **Domain Layer** (`domain/`): **No dependencies** - Contains pure business logic, models, and interfaces
- **Database Layer** (`database/`): **Depends on Domain** - Implements domain interfaces for data persistence
- **CLI Layer** (`cli/`): **Depends on Domain + Database** - Orchestrates use cases and handles user interaction

### Layer Descriptions

#### Domain Layer (`src/bridge/domain/`)

- **Models**: Core business entities (`User`)
- **Services**: Business logic handlers (`CreateUser`, `UpdateUser`, `DeleteUser`, `FetchAllUsers`)
- **Interfaces**: Abstract storage contracts (`UserStorage`)
- **Zero external dependencies** - ensures business logic remains pure and testable

#### Database Layer (`src/bridge/database/`)

- **Core**: Database engine and connection management
- **Storages**: Concrete implementations of domain interfaces (`PostgresUserStorage`)
- **Tables**: SQLAlchemy table definitions
- **Migrations**: Alembic database schema versioning

#### CLI Layer (`src/bridge/cli/`)

- **Commands**: User-facing CLI commands for user and database management
- **App**: CLI application setup and command registration
- **Decorators**: Utilities for async database connection handling

## TODO

- **Data Synchronisation**: Setup data synchronisation with [DummyJSON Users API](https://dummyjson.com/docs/users) to fetch and sync external user data into the local database
