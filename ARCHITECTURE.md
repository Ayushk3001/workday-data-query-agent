# System Architecture: Workday Data Query and Reporting Agent

## 1. High-Level Architecture Overview

The system is designed as a lightweight, schema-grounded natural-language-to-SQL reporting agent. It processes user questions via a LangGraph state graph orchestrating RAG schema retrieval, SQL generation, safety validation, read-only database execution, answer synthesis, and RAGAS-style faithfulness verification.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           React + Vite Frontend                         │
│   [ User Input Bar | Answer & Table Display | SQL Inspector | History ]  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ HTTP / REST API
┌────────────────────────────────────▼────────────────────────────────────┐
│                             FastAPI Backend                             │
│                  [/api/query, /api/schema, /api/history]                │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ Invokes Agent Workflow
┌────────────────────────────────────▼────────────────────────────────────┐
│                        LangGraph State Orchestrator                     │
│                                                                         │
│  ┌───────────────────┐    ┌───────────────────┐   ┌──────────────────┐  │
│  │ 1. Schema RAG     ├───►│ 2. Ambiguity &    ├──►│ 3. SQL           │  │
│  │    Retriever      │    │    Scope Check    │   │    Generation    │  │
│  └─────────┬─────────┘    └─────────┬─────────┘   └────────┬─────────┘  │
│            │ (ChromaDB)             │                      │            │
│            │                        ▼ Refusal/Clarify      ▼            │
│  ┌─────────┴─────────┐    ┌───────────────────┐   ┌────────┴─────────┐  │
│  │ Data Dictionary   │    │ Return Response / │   │ 4. SQL Safety    │  │
│  │ Markdown Index    │    │ Clarification     │   │    Validation    │  │
│  └───────────────────┘    └───────────────────┘   └────────┬─────────┘  │
│                                                            │            │
│  ┌───────────────────┐    ┌───────────────────┐   ┌────────▼─────────┐  │
│  │ 7. Output Result  │◄───┤ 6. Faithfulness   │◄──┤ 5. Read-Only DB  │  │
│  │    + Table        │    │    Self-Check     │   │    Execution     │  │
│  └───────────────────┘    └───────────────────┘   └────────┬─────────┘  │
│                                                            │ (SQLite)   │
│                                                   ┌────────▼─────────┐  │
│                                                   │   workday_hr.db  │  │
│                                                   └──────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. End-to-End Execution Flow

1. **User Question Input**: The user inputs a natural-language HR query via the React UI (e.g., *"How many employees are currently on leave by region?"* or follow-up *"Break that down by department"*).
2. **Schema Retrieval via RAG**: The agent queries ChromaDB (populated with chunks of `data_dictionary.md`) to extract relevant table structures, columns, relationships, and value definitions based on query semantics.
3. **Ambiguity & Scope Verification**: The agent checks if the required entities and columns exist in the retrieved schema.
   - *If out-of-scope or ambiguous*: Transition directly to generating a polite clarifying question or refusal without attempting SQL generation.
   - *If valid & grounded*: Proceed to SQL generation.
4. **SQLite SQL Generation**: The LLM drafts an SQLite-compatible query using ONLY retrieved schema elements, incorporating prior conversation memory (`last_sql_query`, `chat_history`) for follow-up drill-downs.
5. **SQL Safety Validation**: The SQL string is passed to a strict parser tool:
   - Validates that the statement starts with `SELECT` or `WITH ... SELECT`.
   - Rejects any multi-statement queries or disallowed keywords (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, `REPLACE`, `PRAGMA`, `ATTACH`, `VACUUM`).
   - *If validation fails*: Triggers a SQL rewrite turn.
6. **SQLite Query Execution**: The validated single-statement read-only SQL is executed against `workday_hr.db`. The raw tabular dataset (headers + rows) is returned.
7. **Natural-Language Answer Generation**: An LLM node drafts a concise, professional summary answer tailored for HR/IT leaders using the raw SQL execution results.
8. **Faithfulness Self-Check**: A RAGAS-style verification node compares the generated text answer against the raw SQL execution output table.
   - Ensures no hallucinated numbers or figures missing from the dataset are presented.
   - If inconsistent, auto-corrects the response before returning.
9. **Final Response Delivery**: FastAPI returns the natural-language answer, supporting result table, validated SQL query, and execution metadata to the React frontend.

---

## 3. Major Component Responsibilities

### 1. React + Vite Frontend
- **Responsibilities**:
  - Provides a clean, modern user interface for asking questions.
  - Displays natural-language answers alongside interactive data result tables.
  - Features an expandable SQL Query Inspector showing the executed SQLite query.
  - Displays a Query History sidebar/view.
  - Manages multi-turn conversation UI state for follow-up questions.

### 2. FastAPI Backend Service
- **Responsibilities**:
  - Serves REST endpoints (`POST /api/query`, `GET /api/schema`, `GET /api/history`).
  - Handles request validation and delegates execution to the LangGraph agent graph.
  - Manages session lifecycle and state serialization.

### 3. Schema RAG Retriever (ChromaDB)
- **Responsibilities**:
  - Indexes structured descriptions from `data_dictionary.md` (tables, column names, data types, primary/foreign keys, allowed status codes).
  - Performs semantic retrieval to provide targeted schema context to the SQL generator node.

### 4. LangGraph State Agent
- **State Schema**:
  - `question`: Current user input string.
  - `chat_history`: History of previous user and assistant turns.
  - `retrieved_schema`: Context string retrieved from ChromaDB.
  - `is_ambiguous`: Boolean flag indicating if query is out-of-scope or needs clarification.
  - `generated_sql`: Current drafted SQL query string.
  - `sql_valid`: Boolean flag for SQL safety validation status.
  - `query_results`: Dictionary containing column names and row data.
  - `draft_answer`: Natural-language answer text.
  - `faithfulness_passed`: Verification status flag.
  - `final_answer`: Verified final natural-language response.
- **Responsibilities**:
  - Orchestrates node transitions in a deterministic graph flow.
  - Retains state memory across conversation turns to handle follow-up drill-downs seamlessly.

### 5. SQL Safety & Read-Only DB Execution Engine
- **Responsibilities**:
  - Performs static inspection/parsing of generated SQL strings to ensure zero mutation capability.
  - Connects to `workday_hr.db` with read-only connection flags.
  - Formats query outputs into raw structured tables for answer generation and UI rendering.

### 6. Faithfulness Checker Node
- **Responsibilities**:
  - Evaluates the generated natural-language draft against raw database results.
  - Ensures numerical figures, counts, averages, and names in the textual response match exact values in the query output table.

---

## 4. Satisfying PDF Requirements

| PDF Requirement | Architectural Solution |
| :--- | :--- |
| **SQL Generation Accuracy (40%)** | RAG retriever provides exact schema context; SQL generator prompt is strictly constrained by retrieved schema and conversation history memory. |
| **Answer Faithfulness (35%)** | Dedicated Faithfulness Self-Check node compares the final answer against raw database execution results before responding. |
| **Schema-Grounding & Safety (25%)** | ChromaDB RAG schema index prevents ungrounded queries; AST SQL validator blocks non-`SELECT` keywords and multi-statement queries. |
| **Refuse / Clarify Ambiguous Asks** | Pre-generation Ambiguity & Scope Check node detects missing schema targets or ambiguous requests and returns clarification instead of executing SQL. |
| **Follow-Up Drill-Down Support** | LangGraph conversation memory preserves `chat_history` and `last_sql_query` state for multi-turn context reuse without regenerating from scratch. |
| **User Interface Expectations** | React + Vite dashboard displaying natural-language answers, supporting result tables, query inspector, and query history. |
