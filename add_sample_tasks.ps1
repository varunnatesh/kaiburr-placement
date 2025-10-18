# PowerShell script to add sample tasks to the database
$baseUrl = "http://127.0.0.1:64835/api/tasks"

# Task 1
$task1 = @{
    id = "1"
    name = "Deploy Application"
    owner = "John Doe"
    command = "echo Deploying app"
} | ConvertTo-Json

Invoke-RestMethod -Uri $baseUrl -Method Post -Body $task1 -ContentType "application/json"
Write-Host "Task 1 created: Deploy Application (John Doe)"

# Task 2
$task2 = @{
    id = "2"
    name = "Run Tests"
    owner = "Jane Smith"
    command = "echo Running tests"
} | ConvertTo-Json

Invoke-RestMethod -Uri $baseUrl -Method Post -Body $task2 -ContentType "application/json"
Write-Host "Task 2 created: Run Tests (Jane Smith)"

# Task 3
$task3 = @{
    id = "3"
    name = "Database Backup"
    owner = "John Doe"
    command = "echo Backing up database"
} | ConvertTo-Json

Invoke-RestMethod -Uri $baseUrl -Method Post -Body $task3 -ContentType "application/json"
Write-Host "Task 3 created: Database Backup (John Doe)"

# Task 4
$task4 = @{
    id = "4"
    name = "Deploy Frontend"
    owner = "Alice Johnson"
    command = "echo Deploying frontend"
} | ConvertTo-Json

Invoke-RestMethod -Uri $baseUrl -Method Post -Body $task4 -ContentType "application/json"
Write-Host "Task 4 created: Deploy Frontend (Alice Johnson)"

# Task 5
$task5 = @{
    id = "5"
    name = "Monitor System"
    owner = "Bob Wilson"
    command = "echo Monitoring system"
} | ConvertTo-Json

Invoke-RestMethod -Uri $baseUrl -Method Post -Body $task5 -ContentType "application/json"
Write-Host "Task 5 created: Monitor System (Bob Wilson)"

Write-Host "`nAll tasks created successfully!"
Write-Host "You can now test search by:"
Write-Host "  - Name: 'Deploy', 'Test', 'Backup', etc."
Write-Host "  - Owner: 'John Doe', 'Jane Smith', 'Alice Johnson', 'Bob Wilson'"
