# Download and Install Java 21 LTS (Temurin/Eclipse Adoptium)

Write-Host "=== Downloading Java 21 LTS ===" -ForegroundColor Green

# Create download directory
$downloadDir = "C:\Java"
if (-not (Test-Path $downloadDir)) {
    New-Item -ItemType Directory -Path $downloadDir -Force
}

# Java 21 Download URL (Temurin - Eclipse Adoptium)
$javaUrl = "https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.5%2B11/OpenJDK21U-jdk_x64_windows_hotspot_21.0.5_11.zip"
$javaZip = "$downloadDir\java21.zip"
$javaExtractPath = "$downloadDir\java21"

Write-Host "Downloading Java 21..." -ForegroundColor Cyan
try {
    # Download Java 21
    Invoke-WebRequest -Uri $javaUrl -OutFile $javaZip -UseBasicParsing
    Write-Host "Download complete!" -ForegroundColor Green
    
    # Extract
    Write-Host "Extracting Java 21..." -ForegroundColor Cyan
    Expand-Archive -Path $javaZip -DestinationPath $javaExtractPath -Force
    
    # Find the actual Java directory
    $javaHome = Get-ChildItem -Path $javaExtractPath -Directory | Select-Object -First 1
    
    Write-Host "`n=== Java 21 Installation Complete ===" -ForegroundColor Green
    Write-Host "Java installed at: $($javaHome.FullName)" -ForegroundColor Cyan
    Write-Host "`nTo use Java 21, run:" -ForegroundColor Yellow
    Write-Host "`$env:JAVA_HOME=`"$($javaHome.FullName)`"" -ForegroundColor White
    Write-Host "`$env:Path=`"`$env:JAVA_HOME\bin;`$env:Path`"" -ForegroundColor White
    Write-Host "java -version" -ForegroundColor White
    
    Write-Host "`nTo set permanently (requires admin):" -ForegroundColor Yellow
    Write-Host "[System.Environment]::SetEnvironmentVariable('JAVA_HOME', '$($javaHome.FullName)', 'Machine')" -ForegroundColor White
    Write-Host "[System.Environment]::SetEnvironmentVariable('Path', `"`$env:Path;$($javaHome.FullName)\bin`", 'Machine')" -ForegroundColor White
    
} catch {
    Write-Host "Error downloading Java 21: $_" -ForegroundColor Red
    Write-Host "`nAlternative: Please download Java 21 manually from:" -ForegroundColor Yellow
    Write-Host "https://adoptium.net/temurin/releases/?version=21" -ForegroundColor Cyan
}
