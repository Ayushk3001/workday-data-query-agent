# Workday Data Query and Reporting Agent

An AI-powered HR analytics application that allows users to ask natural-language questions about a fictional Workday-style HR database.

## Example Question

> How many employees are currently on leave by region?

## Expected Workflow

User Question
↓
Schema Retrieval using RAG
↓
SQLite SQL Generation
↓
SQL Validation
↓
SQLite Query Execution
↓
Natural-Language Answer
↓
Faithfulness Check
↓
Answer + Supporting Results Table

## Technology Stack

- Python
- FastAPI
- SQLite
- LangGraph
- ChromaDB
- React + Vite

## Planned Database

The fictional HR database will include:

- Departments
- Regions
- Employees
- Leave Records
- Job Openings

All data will be synthetic.

## Key Features

- Natural-language HR questions
- Schema-aware SQL generation
- RAG-based schema grounding
- Read-only SQL validation
- SQLite query execution
- Natural-language answers
- Supporting result tables
- Answer faithfulness checking
- Basic follow-up questions

## Development Phases

- [ ] Phase 1: Project planning
- [ ] Phase 2: SQLite database and synthetic data
- [ ] Phase 3: FastAPI backend foundation
- [ ] Phase 4: Data dictionary
- [ ] Phase 5: Schema RAG
- [ ] Phase 6: SQL generation
- [ ] Phase 7: SQL validation and execution
- [ ] Phase 8: LangGraph workflow
- [ ] Phase 9: Answer generation and faithfulness check
- [ ] Phase 10: React frontend

## Project Goal

The final application should allow a user to ask a natural-language HR question. The system will retrieve the relevant database schema, generate safe SQLite SQL, execute it, and return a faithful answer with supporting data.
