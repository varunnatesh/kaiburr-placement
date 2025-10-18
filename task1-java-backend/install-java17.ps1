# Download and Install Java 17 (Temurin/Eclipse Adoptium)

Write-Host "=== Downloading Java 17 ===" -ForegroundColor Green

# Create download directory
$downloadDir = "C:\Java"
if (-not (Test-Path $downloadDir)) {
    New-Item -ItemType Directory -Path $downloadDir -Force
}

# Java 17 Download URL (Temurin - Eclipse Adoptium)
$javaUrl = "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.9%2B9/OpenJDK17U-jdk_x64_windows_hotspot_17.0.9_9.zip"
$javaZip = "$downloadDir\java17.zip"
$javaExtractPath = "$downloadDir\java17"

Write-Host "Downloading Java 17..." -ForegroundColor Cyan
try {
    # Download Java 17
    Invoke-WebRequest -Uri $javaUrl -OutFile $javaZip -UseBasicParsing
    Write-Host "Download complete!" -ForegroundColor Green
    
    # Extract
    Write-Host "Extracting Java 17..." -ForegroundColor Cyan
    Expand-Archive -Path $javaZip -DestinationPath $javaExtractPath -Force
    
    # Find the actual Java directory
    $javaHome = Get-ChildItem -Path $javaExtractPath -Directory | Select-Object -First 1
    
    Write-Host "`n=== Java 17 Installation Complete ===" -ForegroundColor Green
    Write-Host "Java installed at: $($javaHome.FullName)" -ForegroundColor Cyan
    Write-Host "`nTo use Java 17, run:" -ForegroundColor Yellow
    Write-Host "`$env:JAVA_HOME=`"$($javaHome.FullName)`"" -ForegroundColor White
    Write-Host "`$env:Path=`"`$env:JAVA_HOME\bin;`$env:Path`"" -ForegroundColor White
    Write-Host "java -version" -ForegroundColor White
    
} catch {
    Write-Host "Error downloading Java 17: $_" -ForegroundColor Red
    Write-Host "`nAlternative: Please download Java 17 manually from:" -ForegroundColor Yellow
    Write-Host "https://adoptium.net/temurin/releases/?version=17" -ForegroundColor Cyan
}
