# Invoices

An invoice management application built with Domain-Driven Design principles, featuring a RESTful API, a CLI for database management, and an SQLite persistence layer.

## Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1.  Clone the repository and navigate to the project directory
2.  Install dependencies and set up the development environment:

```bash
make init
```

### Run the application

```bash
# 1. Load environment variables:
source .envrc

# 2. Run the server:
make serve

# 3. Call the API:
curl http://localhost:8080/invoices
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
make serve    # Run the server locally
```

### Usage

After installation, you can use the CLI tool for database management:

```bash
invoices database upgrade head    # Apply database migrations
invoices database current         # Show current migration version
invoices database history         # List changeset scripts in chronological order
invoices database revision        # Create a new revision
invoices database downgrade base  # Revert all migrations
```

## Project Architecture

This project follows **Domain-Driven Design (DDD)** principles with a clean layered architecture:

```
src/invoices/
├── apps/          # Application Layer (server, cli)
├── core/          # Core Layer (config, utils)
├── domain/        # Domain Layer (core business logic)
└── database/      # Infrastructure/Persistence Layer
```

### Layer Dependencies

The architecture enforces strict dependency rules:

- **Core Layer** (`core/`): **No dependencies** - Contains the application's configuration and shared utilities.
- **Domain Layer** (`domain/`): **Depends on Core** - Contains pure business logic, models, and interfaces.
- **Database Layer** (`database/`): **Depends on Core + Domain** - Implements domain interfaces for data persistence.
- **Application Layer** (`apps/`): **Depends on Core + Domain + Database** - Orchestrates use cases and handles user interaction.

### Layers Overview

The **Invoices** application is built upon a strict layered architecture designed to ensure a clean separation of concerns and high testability. By enforcing a unidirectional dependency flow, the system keeps its core business logic isolated from external frameworks and infrastructure details.

At the center of the system is the **Core Layer**. This serves as the foundational bedrock, providing essential configuration management and shared utility functions—such as case-enforcement and UUID validation—without depending on any other internal layers. This zero-dependency stance ensures that fundamental tools remain pure and globally accessible.

Building upon the core is the **Domain Layer**, which houses the heart of the application. It defines the "what" of the system through pure business models like the Invoice, and describes the "how" through service handlers like FetchAllInvoices. Crucially, this layer defines the InvoiceStorage interface, establishing a contract for data persistence without concerning itself with whether that data lives in a database or in memory.

The **Database Layer** acts as an implementation detail of the domain's contracts. It depends on both the Core and Domain layers to provide concrete storage solutions, such as the DatabaseInvoiceStorage. This layer manages the technicalities of the infrastructure, including SQLAlchemy table definitions, engine management, and schema evolution via Alembic migrations.

Finally, the **Application Layer** serves as the orchestrator and entry point for the entire system. It depends on all underlying layers to bridge the gap between user intent and business logic. This layer is split into two primary interfaces: a Server component that exposes a RESTful API via Starlette, and a CLI component that provides administrative commands. By utilizing dependency injection, the Application layer assembles the concrete database implementations into the domain services, delivering a fully functional and decoupled experience to the end user.
