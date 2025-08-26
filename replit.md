# Overview

Neural Dream Weaver is a Brain-Computer Interface (BCI) simulation web application that provides real-time health monitoring, dream analysis, and AI-powered wellness insights. The application uses a modern full-stack architecture with React for the frontend, Express for the backend, and integrates with OpenAI for intelligent analysis of user data including mood tracking and dream interpretation.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: React with TypeScript using Vite for build tooling and development server
- **UI Library**: Shadcn/ui components built on Radix UI primitives for accessible design system
- **Styling**: Tailwind CSS with custom neural-themed color palette and glass morphism effects
- **State Management**: TanStack Query for server state management and caching
- **Routing**: Wouter for lightweight client-side routing
- **Charts**: Chart.js for data visualization (EEG waves, mood trends, sleep patterns)

## Backend Architecture
- **Framework**: Express.js with TypeScript
- **API Design**: RESTful endpoints for health metrics, dream analysis, AI chat, and user settings
- **Request Handling**: JSON middleware with comprehensive error handling and request logging
- **Development**: Hot module replacement with Vite integration for seamless development experience

## Data Storage Solutions
- **Database**: PostgreSQL with Drizzle ORM for type-safe database operations
- **Schema**: Structured tables for users, health metrics, dream analysis, AI chats, and user settings
- **Migrations**: Drizzle Kit for database schema management and migrations
- **Fallback**: In-memory storage implementation for development and testing scenarios

## Authentication and Authorization
- **Session Management**: Express sessions with PostgreSQL session store (connect-pg-simple)
- **User Management**: User creation and authentication through the storage layer
- **Security**: Environment-based configuration with secure session handling

## External Dependencies

- **OpenAI Integration**: GPT-5 model for mood analysis, dream interpretation, and AI chat functionality
- **Database Provider**: Neon Database (serverless PostgreSQL) for production data storage
- **UI Components**: Radix UI ecosystem for accessible, unstyled component primitives
- **Development Tools**: ESBuild for production bundling, TypeScript for type safety
- **Styling Dependencies**: Tailwind CSS with custom fonts (Orbitron, Inter) for futuristic theming

The application implements a modular architecture with clear separation between client and server code, shared schema definitions, and comprehensive error handling throughout the stack.