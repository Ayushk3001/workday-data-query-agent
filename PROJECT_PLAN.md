# Project Plan: Workday Data Query and Reporting Agent

## 1. Key Requirements (Extracted from Problem Statement PDF)

### Business Scenario & Objective
HR and IT leaders need instant, plain-English answers to ad hoc HR questions (e.g., headcount on leave by region, average time-to-fill for open positions) without waiting days for custom report generation. The system must retrieve appropriate schema context via RAG, generate and validate SQLite SQL, execute read-only queries, and synthesize faithful natural-language answers backed by raw tabular data.

### Primary Evaluation Rubric
1. **SQL Generation Accuracy (40%)**: Generated SQL queries must return correct results verified against ground-truth query sets.
2. **Answer Faithfulness (35%)**: A RAGAS-style evaluation check must confirm that final natural-language answers strictly reflect actual query execution results without inventing figures.
3. **Schema-Grounding & Safety (25%)**: The agent must reference only actual database schemas retrieved via RAG, reject out-of-scope or ungrounded table/column requests, and enforce strict read-only execution.

### Key Constraints & Functional Requirements
- **No Hallucinated Schemas**: Prevent generating SQL against non-existent tables or columns. If requested information is unavailable, refuse or ask for clarification instead of guessing.
- **Ambiguity & Out-of-Scope Handling**: Detect ambiguous or ungrounded requests and ask clarifying questions instead of executing faulty SQL.
- **Follow-Up Drill-Downs**: Preserve conversation history and state memory to allow natural follow-up queries (e.g., "now break that down by department") without starting from scratch.
- **SQL Safety**: Only `SELECT` and `WITH ... SELECT` queries are allowed. Multi-statement queries and data manipulation statements (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, `PRAGMA`, etc.) must be rejected.
- **Faithfulness Verification**: Self-check step comparing generated textual answers against raw SQL result sets before presenting to the user.

---

## 2. Feature Specification

### Required Features (Mandatory)
- [x] **Schema Grounding via RAG**: Data dictionary indexing using ChromaDB to retrieve relevant table/column metadata for incoming user prompts.
- [x] **Schema-Aware SQLite SQL Generation**: LLM-driven query generator constrained strictly to retrieved schema definitions.
- [x] **Strict SQL Validation & Safety Tool**: AST/Parser validation allowing only single-statement `SELECT` / `WITH...SELECT` queries.
- [x] **Safe Query Execution Engine**: Read-only SQLite connector returning structured tabular datasets.
- [x] **Natural-Language Answer Generation**: Plain-English response formatting tailored for business users.
- [x] **RAGAS-Style Faithfulness Checker**: Self-verification node comparing natural-language answers against execution results to prevent hallucinated numbers.
- [x] **Ambiguity & Refusal Handler**: Clarification node triggered when user questions are ambiguous or refer to non-existent data.
- [x] **Conversation Memory & Drill-down Context**: LangGraph state management retaining prior SQL context and conversation turn details for drill-down follow-ups.
- [x] **Web User Interface**: React + Vite frontend featuring question input, formatted natural-language answer display, interactive results table, SQL query inspector, and query history view.

### Optional Features (Can be skipped if time is limited)
- [ ] Complex multi-chart data visualization in frontend (standard tabular results are required).
- [ ] Export query results to CSV/Excel formats.
- [ ] Advanced user authentication or role-based table access controls.
- [ ] External database engines (e.g., PostgreSQL/MySQL) — stick strictly to SQLite as specified.

---

## 3. Phase-by-Phase Implementation Plan

### Phase 1: Project Planning & Architecture (Current Phase)
- **Tasks**: Analyze requirements from PDF, CLAUDE.md, and README.md. Draft `PROJECT_PLAN.md` and `ARCHITECTURE.md`.
- **Success Criteria**: Formalized project plan and minimal architecture approved without starting application code or database generation.

### Phase 2: SQLite HR Database & Synthetic Data Generation
- **Tasks**: Create SQLite database (`workday_hr.db`) with 5 core tables (`departments`, `regions`, `employees`, `leave_records`, `job_openings`). Seed synthetic data (minimum 8 departments, 6 regions, 500 employees, 150 leave records, 50 job openings).
- **Success Criteria**: Verified SQLite database with primary/foreign keys and realistic test data populated.

### Phase 3: Data Dictionary Definition & FastAPI Foundation
- **Tasks**: Create comprehensive `data_dictionary.md` containing table schema descriptions, column data types, allowed values, and relationship descriptions. Set up basic FastAPI application skeleton.
- **Success Criteria**: Clean `data_dictionary.md` file and functioning FastAPI server endpoints.

### Phase 4: Schema RAG Engine (ChromaDB Integration)
- **Tasks**: Implement text chunking and vector indexing of `data_dictionary.md` in ChromaDB. Build schema retrieval tool to fetch relevant tables and columns for a given user query.
- **Success Criteria**: Retrieval tool returns accurate table/column context for sample HR questions.

### Phase 5: SQL Generation, Safety Validator & Safe DB Execution
- **Tasks**: Implement prompt template for schema-grounded SQL generation. Build strict SQL validator (allowing `SELECT`/`WITH...SELECT` only; rejecting unsafe syntax or multi-statements). Implement read-only database execution tool.
- **Success Criteria**: Valid SQL generated for sample questions; unsafe SQL statements consistently blocked; read-only query results returned as JSON.

### Phase 6: LangGraph Agent & Conversation Memory Integration
- **Tasks**: Build sequential LangGraph workflow connecting Schema RAG, SQL Generation, SQL Validation, DB Execution, Answer Generation, and Faithfulness Check. Add state memory for follow-up drill-downs.
- **Success Criteria**: Agent executes end-to-end workflow; follow-up questions successfully reuse previous query context.

### Phase 7: Natural-Language Answer Synthesis & Faithfulness Check
- **Tasks**: Implement Answer Generation node converting query results into clear English. Implement RAGAS-style Faithfulness Check node verifying numerical accuracy against raw SQL output.
- **Success Criteria**: Faithful answers generated; numerical discrepancies or hallucinated facts flagged and revised before response delivery.

### Phase 8: Ambiguity & Out-of-Scope Refusal Logic
- **Tasks**: Add guardrail logic to detect requests referencing missing schema elements or ambiguous parameters, triggering a clarifying question instead of generating faulty SQL.
- **Success Criteria**: Out-of-scope and ambiguous queries reliably produce polite clarifying responses without running SQL.

### Phase 9: React Frontend Dashboard
- **Tasks**: Build responsive React + Vite UI with question input box, answer text card, interactive results table, query inspector (viewing generated SQL), and query history log.
- **Success Criteria**: Full UI integration communicating seamlessly with FastAPI backend endpoints.

### Phase 10: End-to-End Verification & Rubric Testing
- **Tasks**: Test full stack against standard HR query set, follow-up drill-down sequences, and red-team/out-of-scope query set.
- **Success Criteria**: All rubric criteria satisfied (SQL Accuracy 40%, Answer Faithfulness 35%, Schema-Grounding & Safety 25%).

---

## 4. Key Assumptions

1. **Synthetic Data Sufficiency**: A well-structured synthetic SQLite database with 5 tables and sufficient record volume is fully adequate to evaluate ground-truth SQL accuracy.
2. **LLM Provider**: The backend will utilize OpenAI/LangChain-compatible LLM endpoints for schema RAG, SQL drafting, answer generation, and faithfulness checks.
3. **Local Vector Store**: ChromaDB will serve as the lightweight, embedded vector store for schema and data dictionary retrieval without requiring cloud infrastructure.
4. **Single-Database Context**: All queries operate against the single local `workday_hr.db` SQLite database in read-only mode.
