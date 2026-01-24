# Invoices

An invoice management application built with Next.js, featuring a clean separation between data and UI, and an in-memory persistence layer.

## Getting Started

### Prerequisites

- Node.js (v20 or later recommended)
- npm

### Installation

1.  Clone the repository and navigate to the project directory.
2.  Install dependencies:

```bash
npm install
```

### Running the Development Server

To run the application in development mode:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

### Available Commands

The project uses npm scripts for common development tasks:

```bash
npm run dev     # Start the development server
npm run build   # Build the application for production
npm run start   # Start the production server
npm run lint    # Run the Biome linter and type checker
npm run format  # Format code with Biome
```

## Project Architecture

The project is organized into three main layers to create a clear and simple structure:

```
/
├── app/            # Main application pages and logic
├── components/     # Reusable, shared UI components
└── lib/            # Core data models and persistence logic
```

**The Data Layer (lib/)**

The lib layer constitutes the intellectual heart of the application. Its primary responsibility is to define the "truth" of the data through rigorous validation schemas using Zod. By combining data structure definitions with TypeScript type inference, this layer guarantees that no information can circulate within the system without conforming to business expectations.

Within this layer, Models act as pure entities, while Stores manage persistence. Although currently implemented in-memory, these stores simulate the behavior of an asynchronous database infrastructure, centralizing all data manipulation operations. They safeguard system integrity by validating every input and output, thereby isolating the rest of the application from the complexities of storage.

**The Component Layer (components/)**

The components layer is dedicated to atomic and reusable visual presentation. Its responsibility is to provide generic, accessible, and aesthetically consistent UI tools. By leveraging robust primitives like Radix UI, this layer focuses exclusively on visual behavior and low-level interaction. The components here are "dumb": they have no knowledge of invoices or transport orders. They receive instructions via props and communicate through events, allowing them to be reused in any context without modification.

**The Application Layer (app/)**

The app layer serves as the final orchestrator. This is where user needs meet the power of the data models. Its responsibility is to transform generic components into specific business tools, such as invoice cards or transport order management interfaces.

This layer utilizes Server Actions to create a secure and reactive bridge between the browser and the server. When an action is triggered, it coordinates mutations within the stores, manages side effects, and instructs Next.js to intelligently refresh the interface. As the primary entry point of the project, it assembles the navigation, defines page layouts, and handles initial data fetching, providing a seamless user experience where the server and client collaborate transparently.
