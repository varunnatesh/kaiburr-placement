# ⚡ Quick Setup Guide for Task 1

## Current Status
✅ Java 8 is extracted at: `C:\Java\java-1.8.0-openjdk-1.8.0.392-1.b08.redhat.windows.x86_64`
❌ Need Java 17 for Spring Boot 3.2

## 🎯 Quick Solution: Download Java 17

### Option 1: Direct Download (RECOMMENDED - 2 minutes)

1. **Download Java 17:**
   - Visit: https://adoptium.net/temurin/releases/?version=17
   - Click: "Windows x64" under "JDK 17"
   - Download the `.zip` file (NOT .msi, we want portable)
   - Save to: `C:\Users\VARUN\Downloads\`

2. **Extract Java 17:**
   ```powershell
   # After downloading, run this (replace filename if different):
   Expand-Archive -Path "C:\Users\VARUN\Downloads\OpenJDK17*.zip" -DestinationPath "C:\Java\java17" -Force
   ```

3. **Set Java 17 for this session:**
   ```powershell
   $env:JAVA_HOME="C:\Java\java17\jdk-17.0.9+9"
   $env:Path="$env:JAVA_HOME\bin;$env:Path"
   java -version
   ```

---

### Option 2: Use Your Java 8 with Modified Code (Quick Workaround)

Since you have Java 8, I can modify the Spring Boot project to work with Java 8:

**Pros:** Can start immediately
**Cons:** Using older Java version

Would you like me to:
- **A)** Wait for you to download Java 17 (recommended)
- **B)** Modify the project to work with Java 8 (quick start)

---

## 📦 After Java is Set Up

### Install Maven

**Using Chocolatey:**
```powershell
# Install Chocolatey first (run as Administrator):
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Then install Maven:
choco install maven -y
```

**Manual Download:**
1. Visit: https://maven.apache.org/download.cgi
2. Download "Binary zip archive"
3. Extract to `C:\Maven`
4. Add to PATH:
   ```powershell
   $env:Path="C:\Maven\apache-maven-3.9.5\bin;$env:Path"
   ```

### Install MongoDB

**Using Chocolatey:**
```powershell
choco install mongodb -y
```

**Manual Download:**
1. Visit: https://www.mongodb.com/try/download/community
2. Download Windows MSI
3. Install with default settings
4. Start MongoDB service:
   ```powershell
   Start-Service MongoDB
   ```

---

## ⚡ Fast Track

Tell me which option you prefer:
- Type **"17"** - I'll wait for you to download Java 17 
- Type **"8"** - I'll modify the project for Java 8 right now
- Type **"choco"** - Guide me through installing Chocolatey to auto-install everything
