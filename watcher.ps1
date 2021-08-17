if (-Not(Test-Path -Path .\env_activator.ps1))
{
    $venv_path = Read-Host -Prompt 'Enter your python virtual environment folder'
    while (-Not(Test-Path -Path "$venv_path\Scripts\"))
    {
        Write-Output "Invalid path ($venv_path\Scripts\)"
        $venv_path = Read-Host -Prompt 'Try again'
    }

    Write-Output "
Set-Location '$venv_path\Scripts\'
.\activate
Set-Location $PSScriptRoot
    " > env_activator.ps1
}
if (-Not(Test-Path -Path .\.env.develop))
{
    $env = ""
    $sep = "="
    $requiredFields = "BOT_TOKEN", "NOTIFICATION_CHAT"
    foreach ($line in Get-Content .\.env)
    {
        $key, $value = $line.Split($sep)
        if ($key -eq "MODE")
        {
            $env += $key + $sep + "development" + "`n"
        }
        elseif ($requiredFields.Contains($key))
        {
            $value = Read-Host -Prompt $key
            $env += $key + $sep + $value + "`n"
        }
    }
    [IO.File]::WriteAllLines(".\.env.develop", $env)
}
.\env_activator.ps1
