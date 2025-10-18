# Task 1 - Installation Instructions

## Quick Start: What You Need to Install

Since Java and Maven are not currently installed on your system, follow these steps:

### 1️⃣ Install Java JDK 17

**Easiest Method - Using Chocolatey:**

```powershell
# Open PowerShell as Administrator and run:
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Then install Java:
choco install openjdk17 -y
```

**Manual Method:**
- Download from: https://adoptium.net/temurin/releases/?version=17
- Install the Windows x64 .msi installer
- Restart your terminal

### 2️⃣ Install Maven

```powershell
# Using Chocolatey:
choco install maven -y

# Or download manually from:
# https://maven.apache.org/download.cgi
```

### 3️⃣ Install MongoDB

```powershell
# Using Chocolatey:
choco install mongodb -y

# Or download from:
# https://www.mongodb.com/try/download/community
```

### 4️⃣ After Installation

Close and reopen PowerShell, then verify:

```powershell
java -version    # Should show Java 17.x
mvn -version     # Should show Maven 3.x
mongosh --version # Should show MongoDB shell
```

### 5️⃣ Then Run the Application

```powershell
cd c:\placement\task1-java-backend
mvn clean install
mvn spring-boot:run
```

---

## 🎯 Current Status

✅ **Project files created** - All Java code is ready
❌ **Java not installed** - Need JDK 17+
❌ **Maven not installed** - Need Maven 3.6+
❌ **MongoDB not installed** - Need MongoDB 5.0+

## 📋 What to Do Next

1. **Install the prerequisites above** (takes 10-15 minutes)
2. **Run the application**
3. **Test with Postman or PowerShell**
4. **Take screenshots with your name and date visible**
5. **Move to next task**

See **SETUP_GUIDE.md** for detailed step-by-step instructions.

Would you like me to help you with the installation process, or shall we move to Task 3 or Task 5 which can run with the tools you already have (Node.js and Python)?
