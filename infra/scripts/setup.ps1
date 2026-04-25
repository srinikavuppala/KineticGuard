# Kinetic Guard v3.0 - Environment Setup Script
Write-Host "====================================" -ForegroundColor Cyan
Write-Host " Kinetic Guard - Initial Setup" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan

 $envFile = ".env"
 $envExample = ".env.example"

if (Test-Path $envFile) {
    Write-Host "[WARNING] .env file already exists. Skipping copy to prevent overwriting your secrets." -ForegroundColor Yellow
} else {
    Write-Host "[INFO] Creating .env file from .env.example..." -ForegroundColor Green
    Copy-Item $envExample $envFile
    Write-Host "[SUCCESS] .env file created! Please open it and update your passwords." -ForegroundColor Green
}

Write-Host ""
Write-Host "Setup complete! You can now run: docker-compose up --build" -ForegroundColor Cyan