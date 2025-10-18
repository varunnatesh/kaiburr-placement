# Task Manager API Run Report

- User: Varun K N
- Time: 18-10-2025 08:21:26 PM
- Base: http://127.0.0.1:8001/api/v1/namespaces/default/services/http:task-manager:8080/proxy/api/tasks

| Step | Action | Status | Key Info |
|------|--------|--------|----------|
| 1 | GET ALL | OK | count=4 |
| 2 | PUT create/update | OK | id=101, name=Demo Task 101 |
| 3 | GET by id | OK | id=101, name=Demo Task 101 |
| 4 | SEARCH by name | OK | count=1 |
| 5 | SEARCH by owner | OK | count=2 |
| 6 | PUT execute | OK | output='Hello from 101 ' |
| 7 | DELETE | OK | deleted id=101 |
| 8 | GET ALL (final) | OK | count=4 |
