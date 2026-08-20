# Workday Data Query and Reporting Agent

## Project Goal
Build an AI-powered application that answers natural-language questions about a fictional Workday-style HR database.

The system should:
1. Retrieve relevant database schema using RAG.
2. Generate SQLite-compatible SQL.
3. Validate SQL before execution.
4. Execute only safe read-only queries.
5. Return query results and a natural-language answer.
6. Check that the answer is faithful to the actual query results.
7. Support simple follow-up questions.

## Technology Stack
- Python
- FastAPI
- SQLite
- LangGraph
- ChromaDB
- React + Vite

## Core Priorities
1. SQL accuracy
2. Schema grounding
3. SQL safety
4. Answer faithfulness
5. Simple follow-up context
6. Clean UI

Keep the solution simple and testable. Do not add unnecessary features.

## Required Database
Create a fictional Workday-style HR database with:
- departments
- regions
- employees
- leave_records
- job_openings

Use synthetic data only.

Suggested minimum:
- 8 departments
- 6 regions
- 500 employees
- 150 leave records
- 50 job openings

Use meaningful primary keys, foreign keys, and relationships.

## Schema Grounding
The AI must never invent database tables or columns.

Before generating SQL:
1. Retrieve relevant schema context using RAG.
2. Provide that context to the SQL generator.
3. Generate SQL only using available tables and columns.

If requested information does not exist, do not guess.

## SQL Safety
All SQL must be SQLite-compatible.

Allow only:
- SELECT
- WITH ... SELECT

Reject:
- INSERT
- UPDATE
- DELETE
- DROP
- ALTER
- CREATE
- REPLACE
- ATTACH
- DETACH
- PRAGMA
- VACUUM

Never execute multiple SQL statements.

## Target Workflow
START
  ↓
Retrieve Schema
  ↓
Generate SQL
  ↓
Validate SQL
  ↓
Execute SQLite Query
  ↓
Generate Answer
  ↓
Faithfulness Check
  ↓
Answer + Supporting Results

Use LangGraph to orchestrate the workflow only after the individual components work independently.

## RAG
Create a data_dictionary.md containing:
- Tables
- Columns
- Data types
- Descriptions
- Relationships
- Important allowed values

Use ChromaDB for lightweight local schema retrieval.

## Development Principles
### Think Before Coding
Inspect existing files before making significant changes. Understand dependencies and make the smallest change necessary.

### Keep It Simple
Avoid unnecessary:
- Microservices
- Docker
- Authentication
- Cloud infrastructure
- Complex multi-agent systems
- Extra databases
- Unused abstractions

### Make Surgical Changes
Do not rewrite working code unnecessarily. Modify only relevant files and test after changes.

## Development Order
1. Project planning
2. SQLite database and synthetic data
3. FastAPI foundation
4. Data dictionary
5. Schema RAG
6. SQL generation
7. SQL validation and safe execution
8. LangGraph integration
9. Answer generation and faithfulness check
10. React frontend

Do not skip ahead unless explicitly instructed.

## Testing
After every major phase:
1. Run tests or the application.
2. Verify the feature works.
3. Fix errors.
4. Do not proceed if the current phase is broken.

Never claim a feature works without testing it.

## Agent Behavior
Work incrementally. After completing a task:
1. Report what changed.
2. Report test results.
3. Report known limitations.
4. Stop and wait for the next instruction.

Never continue automatically to the next phase.
