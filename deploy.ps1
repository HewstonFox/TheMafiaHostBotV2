Push-Location $PSScriptRoot
Copy-Item -Recurse -Force assets deploy/the-mafia-host-bot/
Copy-Item -Recurse -Force bot deploy/the-mafia-host-bot/
Copy-Item -Recurse -Force .env deploy/the-mafia-host-bot/
Copy-Item -Recurse -Force config.py deploy/the-mafia-host-bot/
Copy-Item -Recurse -Force main.py deploy/the-mafia-host-bot/
Copy-Item -Recurse -Force Procfile deploy/the-mafia-host-bot/
Copy-Item -Recurse -Force requirements.txt deploy/the-mafia-host-bot/
Copy-Item -Recurse -Force runtime.txt deploy/the-mafia-host-bot/
Copy-Item -Recurse -Force .gitignore deploy/the-mafia-host-bot/
Pop-Location