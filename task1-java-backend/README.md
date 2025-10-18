# Task 1: Java Backend REST API

## Project Overview
This is a Spring Boot REST API application for managing and executing tasks. Each task represents a shell command that can be executed, and the execution history is stored.

## Technologies Used
- Java 17
- Spring Boot 3.2.0
- Spring Data MongoDB
- Maven
- Lombok
- MongoDB

## Prerequisites
- Java 17 or higher
- Maven 3.6+
- MongoDB running on localhost:27017 (or configure connection in application.properties)

## Project Structure
```
task1-java-backend/
├── src/
│   └── main/
│       ├── java/com/kaiburr/taskmanager/
│       │   ├── TaskManagerApplication.java
│       │   ├── controller/
│       │   │   └── TaskController.java
│       │   ├── model/
│       │   │   ├── Task.java
│       │   │   └── TaskExecution.java
│       │   ├── repository/
│       │   │   └── TaskRepository.java
│       │   ├── service/
│       │   │   ├── TaskService.java
│       │   │   └── CommandValidationService.java
│       │   └── exception/
│       │       ├── TaskNotFoundException.java
│       │       └── InvalidCommandException.java
│       └── resources/
│           └── application.properties
├── pom.xml
└── README.md
```

## Data Model

### Task Object
```json
{
  "id": "123",
  "name": "Print Hello",
  "owner": "John Smith",
  "command": "echo Hello World!",
  "taskExecutions": [
    {
      "startTime": "2025-10-16T15:51:42.276Z",
      "endTime": "2025-10-16T15:51:43.276Z",
      "output": "Hello World!"
    }
  ]
}
```

## API Endpoints

### 1. Get All Tasks
- **Method:** GET
- **URL:** `http://localhost:8080/api/tasks`
- **Description:** Returns all tasks

### 2. Get Task by ID
- **Method:** GET
- **URL:** `http://localhost:8080/api/tasks?id={taskId}`
- **Description:** Returns a specific task by ID
- **Response:** 200 OK or 404 Not Found

### 3. Search Tasks
- **Method:** GET
- **By Name URL:** `http://localhost:8080/api/tasks/search?name={searchString}`
- **By Owner URL:** `http://localhost:8080/api/tasks/search?owner={ownerSubstring}`
- **Description:** Returns tasks whose name/owner contains the search string (case-insensitive)
- **Response:** 200 OK with a list (empty list if no matches)

### 4. Create/Update Task
- **Method:** PUT
- **URL:** `http://localhost:8080/api/tasks`
- **Body:**
```json
{
  "id": "123",
  "name": "Print Hello",
  "owner": "John Smith",
  "command": "echo Hello World!"
}
```
- **Description:** Creates a new task or updates an existing one. Validates the command for safety.
- **Response:** 200 OK or 400 Bad Request

### 5. Delete Task
- **Method:** DELETE
- **URL:** `http://localhost:8080/api/tasks/{taskId}`
- **Description:** Deletes a task by ID
- **Response:** 200 OK or 404 Not Found

### 6. Execute Task
- **Method:** PUT
- **URL:** `http://localhost:8080/api/tasks/{taskId}/execute`
- **Description:** Executes the command associated with the task and stores the execution result
- **Response:** 200 OK with TaskExecution object or 404 Not Found

## Setup and Running

### 1. Start MongoDB
Make sure MongoDB is running on your system:
```bash
# If using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or start your local MongoDB instance
mongod
```

## Latest API Run (compact)

For concise terminal output and a Markdown summary of the latest end-to-end run, see:

- Markdown report: `c:\placement\_sanity_screenshots\API_RUN_REPORT.md`
- Full JSON responses (each step): `c:\placement\_sanity_screenshots\*.json`

Reproduce a compact run and generate artifacts:

```powershell
kubectl proxy --port=8001
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File c:\placement\run_api_sequence.ps1 -Mode compact -Limit 5 -SaveDir c:\placement\_sanity_screenshots
# Or create a Markdown summary:
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -File c:\placement\run_api_sequence.ps1 -Mode markdown -Limit 5 -SaveDir c:\placement\_sanity_screenshots
```

### 2. Build the Application
```bash
cd task1-java-backend
mvn clean install
```

### 3. Run the Application
```bash
mvn spring-boot:run
```

Or run the JAR file:
```bash
java -jar target/task-manager-1.0.0.jar
```

The application will start on `http://localhost:8080`

## Configuration

The application can be configured via environment variables:

- `MONGODB_URI` - MongoDB connection URI (default: mongodb://localhost:27017/taskmanager)
- `MONGODB_DATABASE` - MongoDB database name (default: taskmanager)

## Command Validation

The application validates commands to prevent execution of potentially dangerous operations. The following are blocked:
- Destructive commands (rm, del, format, etc.)
- Command injection characters (;, |, &, `, $, etc.)
- Network commands (curl, wget, ssh, etc.)
- Privilege escalation (sudo, su, etc.)
- System control commands (shutdown, reboot, etc.)

## Testing with cURL

### Create a Task
```bash
curl -X PUT http://localhost:8080/api/tasks \
  -H "Content-Type: application/json" \
  -d "{\"id\":\"1\",\"name\":\"Print Hello\",\"owner\":\"John Smith\",\"command\":\"echo Hello World!\"}"
```

### Get All Tasks
```bash
curl http://localhost:8080/api/tasks
```

### Get Task by ID
```bash
curl http://localhost:8080/api/tasks?id=1
```

### Search Tasks by Name
```bash
curl http://localhost:8080/api/tasks/search?name=Hello
```

### Execute a Task
```bash
curl -X PUT http://localhost:8080/api/tasks/1/execute
```

### Delete a Task
```bash
curl -X DELETE http://localhost:8080/api/tasks/1
```

## Testing with Postman

1. Import the following collection or create requests manually
2. Set base URL to `http://localhost:8080`
3. Test all endpoints with proper request bodies


## Screenshots

### Backend Build Success
![](screenshots/maven_package_success_2025-10-18_19-12-43.png)

### GET /api/tasks
![](screenshots/api_get_tasks_2025-10-18_19-13-16.png)

### POST /api/tasks
![](screenshots/api_create_task_2025-10-18_19-13-22.png)

### PUT /api/tasks/{id}
![](screenshots/api_update_task_2025-10-18_19-13-29.png)

### DELETE /api/tasks/{id}
![](screenshots/api_delete_task_2025-10-18_19-13-35.png)

### Search Tasks by Name
![](screenshots/api_search_2025-10-18_19-13-40.png)

## Next Steps

This application is the foundation for:
- **Task 2:** Kubernetes deployment with pod-based command execution
- **Task 3:** React frontend integration
- **Task 4:** CI/CD pipeline setup

## Author

[Your Name]
Date: October 16, 2025
