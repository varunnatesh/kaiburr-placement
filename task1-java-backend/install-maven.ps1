# Download and Install Apache Maven

Write-Host "=== Downloading Apache Maven ===" -ForegroundColor Green

# Create download directory
$downloadDir = "C:\Maven"
if (-not (Test-Path $downloadDir)) {
    New-Item -ItemType Directory -Path $downloadDir -Force
}

# Maven Download URL
$mavenVersion = "3.9.9"
$mavenUrl = "https://archive.apache.org/dist/maven/maven-3/$mavenVersion/binaries/apache-maven-$mavenVersion-bin.zip"
$mavenZip = "$downloadDir\maven.zip"
$mavenExtractPath = "$downloadDir"

Write-Host "Downloading Maven $mavenVersion..." -ForegroundColor Cyan
try {
    # Download Maven
    Invoke-WebRequest -Uri $mavenUrl -OutFile $mavenZip -UseBasicParsing
    Write-Host "Download complete!" -ForegroundColor Green
    
    # Extract
    Write-Host "Extracting Maven..." -ForegroundColor Cyan
    Expand-Archive -Path $mavenZip -DestinationPath $mavenExtractPath -Force
    
    $mavenHome = "$downloadDir\apache-maven-$mavenVersion"
    
    Write-Host "`n=== Maven Installation Complete ===" -ForegroundColor Green
    Write-Host "Maven installed at: $mavenHome" -ForegroundColor Cyan
    Write-Host "`nTo use Maven, run:" -ForegroundColor Yellow
    Write-Host "`$env:MAVEN_HOME=`"$mavenHome`"" -ForegroundColor White
    Write-Host "`$env:Path=`"`$env:MAVEN_HOME\bin;`$env:Path`"" -ForegroundColor White
    Write-Host "mvn -version" -ForegroundColor White
    
} catch {
    Write-Host "Error downloading Maven: $_" -ForegroundColor Red
    Write-Host "`nAlternative: Please download Maven manually from:" -ForegroundColor Yellow
    Write-Host "https://maven.apache.org/download.cgi" -ForegroundColor Cyan
}
