$activator_exist = Test-Path -Path .\env_activator.ps1
if ($activator_exist)
{
    .\env_activator.ps1
}
else
{
    $venv_path = Read-Host -Prompt 'Enter your python virtual environment folder'
    while (-Not(Test-Path -Path "$venv_path\Scripts\"))
    {
        echo "Invalid path ($venv_path\Scripts\)"
        $venv_path = Read-Host -Prompt 'Try again'
    }

    echo "
Set-Location '$venv_path\Scripts\'
.\activate
Set-Location $PSScriptRoot
    " > env_activator.ps1
    .\env_activator.ps1
}