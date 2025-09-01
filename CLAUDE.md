# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
```bash
# Quick start (recommended)
chmod +x run.sh
./run.sh

# Manual start
cd backend
uv run uvicorn app:app --reload --port 8000
```

### Dependency Management
```bash
# Install/sync dependencies
uv sync

# Add new dependency
uv add package-name

# Development server with auto-reload
uv run uvicorn app:app --reload --port 8000
```

### Environment Setup
```bash
# Copy environment template and add API key
cp .env.example .env
# Edit .env to add: ANTHROPIC_API_KEY=your_key_here
```

## Architecture Overview

This is a **Retrieval-Augmented Generation (RAG) chatbot** for course materials with a clear separation between frontend, API layer, and RAG processing components.

### Core Architecture Flow
1. **Frontend** (`frontend/`) → Web interface with vanilla JS
2. **FastAPI Backend** (`backend/app.py`) → API endpoints and static file serving
3. **RAG System** (`backend/rag_system.py`) → Main orchestrator
4. **AI Generator** (`backend/ai_generator.py`) → Claude API integration with tool calling
5. **Search Tools** (`backend/search_tools.py`) → Course search functionality
6. **Vector Store** (`backend/vector_store.py`) → ChromaDB semantic search
7. **Document Processor** (`backend/document_processor.py`) → Text chunking and course parsing

### Key Components

**RAG System** (`rag_system.py`): Main orchestrator that coordinates document processing, vector storage, AI generation, and session management. Handles the complete query flow from user input to response.

**Document Processor** (`document_processor.py`): Processes course documents with expected format:
- Line 1: `Course Title: [title]`
- Line 2: `Course Link: [url]`
- Line 3: `Course Instructor: [instructor]`
- Subsequent lines: Lesson markers (`Lesson N: title`) and content

Text is chunked into sentence-based segments with configurable overlap for optimal semantic search.

**AI Generator** (`ai_generator.py`): Handles Claude API interactions with tool calling support. Uses a static system prompt optimized for course materials and implements tool execution flow for search operations.

**Search Tools** (`search_tools.py`): Implements the `CourseSearchTool` that Claude can call to search course content. Supports filtering by course name and lesson number. Uses an abstract `Tool` interface for extensibility.

**Vector Store** (`vector_store.py`): ChromaDB interface for semantic search with course metadata and content chunks. Handles course deduplication and provides unified search interface with filtering.

### Data Models (`models.py`)
- **Course**: Contains title, link, instructor, and lessons list
- **Lesson**: Has lesson number, title, and optional link
- **CourseChunk**: Text content with course/lesson metadata for vector storage

### Configuration (`config.py`)
Centralized configuration using environment variables and dataclass with sensible defaults:
- Anthropic API settings (model: claude-sonnet-4-20250514)
- Embedding model (all-MiniLM-L6-v2)
- Chunk processing settings (800 chars, 100 overlap)
- ChromaDB path and search limits

### Session Management (`session_manager.py`)
Handles conversation history with configurable message limits for context retention across queries.

## Important Implementation Details

### Document Processing
Course documents must follow a specific format with metadata headers and lesson markers. The processor creates contextual chunks by prefixing content with course and lesson information.

### Tool-Based Search
Claude uses a search tool rather than direct RAG retrieval. This allows for more intelligent query processing and source tracking for the frontend.

### Frontend-Backend Communication
Single-page application with vanilla JavaScript that communicates via JSON API. Supports session-based conversations and displays sources from search operations.

### Startup Behavior
Application automatically loads documents from `/docs` folder on startup and creates vector embeddings if they don't exist.

## File Locations
- Web interface accessible at `http://localhost:8000`
- API documentation at `http://localhost:8000/docs`
- Course documents in `/docs` folder (auto-loaded on startup)
- ChromaDB storage in `./chroma_db` (created automatically)
- always use uv to run the server do not use pip directly
- make sure to use uv to manage all dependencies
- use uv to run Python files
- dont run the server using ./run.sh I will start it myself