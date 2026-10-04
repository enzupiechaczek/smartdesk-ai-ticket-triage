# SmartDesk architecture

## Flow

Browser form -> Flask API -> AI model (predict_category) -> priority rule -> SQLite -> dashboard (urgent first)

## Shared contract

```
POST /api/tickets   body: {"subject": "...", "description": "..."}
  201 -> {"id","subject","description","category","confidence","priority","created_at"}
  400 -> {"error": "message"}
GET  /api/tickets   -> list of tickets, urgent first, then newest first
GET  /api/health    -> {"status": "ok", "service": "SmartDesk local API"}

predict_category(text) -> {"category": "access|billing|technical", "confidence": 0.0-1.0}
```

## Groups

| Group | Owns |
|---|---|
| A1 Application Build | frontend, backend, database, priority rule |
| A2 AI Integration | dataset, training, predictor, model card |
| B QA and Validation | test plan, bug reports, release report |

## Azure mapping (for the Day 4 retrospective)

| SmartDesk (local) | Azure |
|---|---|
| Browser page | Azure Static Web Apps |
| Flask API | Managed API with Azure Functions |
| SQLite | Azure Cosmos DB |
| Local classifier | Azure Language, or a model hosted in Azure |
| Local logs | Application Insights |
