# Task 1: Complete Setup and Execution Guide

## 🎯 Objective
Set up and run the Java Backend REST API application

## ⚙️ Prerequisites to Install

### 1. Install Java Development Kit (JDK) 17 or higher

**Option A: Download from Oracle**
1. Visit: https://www.oracle.com/java/technologies/downloads/#java17
2. Download "Windows x64 Installer"
3. Run the installer
4. Verify installation:
```powershell
java -version
javac -version
```

**Option B: Using Chocolatey (Windows Package Manager)**
```powershell
# Install Chocolatey first if you don't have it:
# Run PowerShell as Administrator
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Then install Java
choco install openjdk17 -y
```

### 2. Install Apache Maven

**Option A: Manual Installation**
1. Visit: https://maven.apache.org/download.cgi
2. Download the "Binary zip archive"
3. Extract to `C:\Program Files\Maven`
4. Add to PATH:
   - Search "Environment Variables" in Windows
   - Edit System Environment Variables
   - Add `C:\Program Files\Maven\bin` to PATH
5. Verify:
```powershell
mvn -version
```

**Option B: Using Chocolatey**
```powershell
choco install maven -y
```

### 3. Install MongoDB

**Option A: MongoDB Community Server**
1. Visit: https://www.mongodb.com/try/download/community
2. Download Windows installer
3. Install with default settings
4. MongoDB will run as a Windows service

**Option B: Using Docker (if you prefer)**
```powershell
# Install Docker Desktop first
# Then run MongoDB in a container:
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

**Option C: Using Chocolatey**
```powershell
choco install mongodb -y
```

---

## 🚀 Step-by-Step Execution (After Prerequisites are Installed)

### Step 1: Verify All Prerequisites

Open a NEW PowerShell window and run:

```powershell
# Check Java
java -version
# Should show: java version "17.x.x" or higher

# Check Maven
mvn -version
# Should show: Apache Maven 3.x.x

# Check MongoDB
mongosh --version
# Or check if MongoDB service is running:
Get-Service MongoDB
```

### Step 2: Start MongoDB

If MongoDB is not running:

```powershell
# If installed as Windows service:
Start-Service MongoDB

# OR if using Docker:
docker start mongodb

# OR if installed manually:
cd "C:\Program Files\MongoDB\Server\7.0\bin"
.\mongod.exe --dbpath "C:\data\db"
```

Verify MongoDB is running:
```powershell
mongosh
# You should see MongoDB shell open
# Type 'exit' to quit
```

### Step 3: Build the Application

```powershell
cd c:\placement\task1-java-backend

# Clean and build the project
mvn clean install

# This will:
# - Download all dependencies
# - Compile the code
# - Run tests
# - Create a JAR file in the target/ directory
```

### Step 4: Run the Application

```powershell
# Run using Maven
mvn spring-boot:run

# OR run the JAR file directly
java -jar target/task-manager-1.0.0.jar
```

The application will start on **http://localhost:8080**

You should see output like:
```
  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::                (v3.2.0)

...
Started TaskManagerApplication in 3.456 seconds
```

---

## 🧪 Testing the Application

### Option 1: Using PowerShell (curl equivalent)

Open a NEW PowerShell window:

```powershell
# Test 1: Create a Task
Invoke-RestMethod -Uri "http://localhost:8080/api/tasks" -Method Put -Headers @{"Content-Type"="application/json"} -Body '{
  "id": "1",
  "name": "Print Hello",
  "owner": "John Smith",
  "command": "echo Hello World"
}'

# Test 2: Get All Tasks
Invoke-RestMethod -Uri "http://localhost:8080/api/tasks" -Method Get

# Test 3: Get Task by ID
Invoke-RestMethod -Uri "http://localhost:8080/api/tasks?id=1" -Method Get

# Test 4: Execute Task
Invoke-RestMethod -Uri "http://localhost:8080/api/tasks/1/execute" -Method Put

# Test 5: Search Tasks
Invoke-RestMethod -Uri "http://localhost:8080/api/tasks/search?name=Hello" -Method Get

# Test 6: Delete Task
Invoke-RestMethod -Uri "http://localhost:8080/api/tasks/1" -Method Delete
```

### Option 2: Using Postman

1. Download Postman: https://www.postman.com/downloads/
2. Install and open Postman
3. Create a new collection "Task Manager API"
4. Add requests:

**Request 1: Create Task**
- Method: PUT
- URL: http://localhost:8080/api/tasks
- Body (JSON):
```json
{
  "id": "1",
  "name": "Print Hello",
  "owner": "John Smith",
  "command": "echo Hello World"
}
```

**Request 2: Get All Tasks**
- Method: GET
- URL: http://localhost:8080/api/tasks

**Request 3: Execute Task**
- Method: PUT
- URL: http://localhost:8080/api/tasks/1/execute

**Request 4: Get Task Details**
- Method: GET
- URL: http://localhost:8080/api/tasks?id=1

**Request 5: Search Tasks**
- Method: GET
- URL: http://localhost:8080/api/tasks/search?name=Hello

**Request 6: Delete Task**
- Method: DELETE
- URL: http://localhost:8080/api/tasks/1

### Option 3: Using Browser (for GET requests only)

Open your browser and visit:
- http://localhost:8080/api/tasks (Get all tasks)
- http://localhost:8080/api/tasks?id=1 (Get task by ID)
- http://localhost:8080/api/tasks/search?name=Hello (Search)

---

## 📸 Taking Screenshots for Submission

### Screenshot 1: Prerequisites Installed
Show terminal with:
```powershell
java -version; mvn -version
```
Make sure your **name** and **date/time** are visible!

### Screenshot 2: Application Starting
Show the Spring Boot startup logs with your name visible

### Screenshot 3: Create Task
Show Postman/PowerShell request creating a task

### Screenshot 4: Get All Tasks
Show the response with tasks listed

### Screenshot 5: Execute Task
Show task execution and the output

### Screenshot 6: MongoDB Data
Show MongoDB data:
```powershell
mongosh
use taskmanager
db.tasks.find()
```

### Screenshot 7: Delete Task
Show successful deletion

**IMPORTANT:** Every screenshot must show:
- ✅ Your name (in terminal prompt, Postman, or visible on screen)
- ✅ Current date and time (system clock)

---

## 🐛 Troubleshooting

### Issue 1: "java is not recognized"
**Solution:** Java not installed or not in PATH. Install JDK 17+ and restart terminal.

### Issue 2: "mvn is not recognized"
**Solution:** Maven not installed or not in PATH. Install Maven and restart terminal.

### Issue 3: "Could not connect to MongoDB"
**Solution:** 
```powershell
# Check if MongoDB is running
Get-Service MongoDB

# Start if stopped
Start-Service MongoDB

# Or check connection
mongosh
```

### Issue 4: "Port 8080 is already in use"
**Solution:** Stop other applications using port 8080 or change the port in `application.properties`:
```properties
server.port=8081
```

### Issue 5: Build fails with dependency errors
**Solution:**
```powershell
# Clear Maven cache and rebuild
mvn clean
mvn dependency:purge-local-repository
mvn clean install
```

---

## ✅ Success Criteria

You have successfully completed Task 1 when:
- ✅ Application starts without errors
- ✅ You can create tasks via API
- ✅ You can retrieve tasks
- ✅ You can execute tasks and see output
- ✅ You can search tasks by name
- ✅ You can delete tasks
- ✅ Data persists in MongoDB
- ✅ You have screenshots with your name and date

---

## 📝 Quick Reference Commands

```powershell
# Start MongoDB
Start-Service MongoDB

# Build application
cd c:\placement\task1-java-backend
mvn clean install

# Run application
mvn spring-boot:run

# Test API (create task)
Invoke-RestMethod -Uri "http://localhost:8080/api/tasks" -Method Put -Headers @{"Content-Type"="application/json"} -Body '{"id":"1","name":"Test","owner":"Your Name","command":"echo Hello"}'

# Test API (get tasks)
Invoke-RestMethod -Uri "http://localhost:8080/api/tasks" -Method Get

# Stop application
Ctrl + C in the terminal running the app
```

---

## 🎓 Understanding the Code

Before submitting, make sure you understand:

1. **Spring Boot Architecture**
   - Controllers handle HTTP requests
   - Services contain business logic
   - Repositories interact with MongoDB
   - Models define data structure

2. **REST API Endpoints**
   - GET = Retrieve data
   - PUT = Create/Update data
   - DELETE = Remove data

3. **MongoDB Integration**
   - Document-based NoSQL database
   - Collections store JSON-like documents
   - Spring Data MongoDB provides easy integration

4. **Command Validation**
   - Prevents dangerous commands
   - Checks for malicious patterns
   - Security best practice

---

## 📞 Next Steps

After completing Task 1:
1. Take all required screenshots
2. Add screenshots to README.md
3. Test everything one more time
4. Create GitHub repository
5. Push code to GitHub
6. Proceed to Task 2 (Kubernetes)

Good luck! 🚀
