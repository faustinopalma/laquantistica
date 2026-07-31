# Apre un capitolo nel browser in modalita' modifica.
#
#   .\modifica.ps1            -> elenca i capitoli e chiede quale
#   .\modifica.ps1 02         -> apre il capitolo 2
#   .\modifica.ps1 rutherford -> apre la pagina il cui nome contiene "rutherford"
#
# Nel browser: doppio clic sul testo o su una formula per correggerli, le frecce
# che compaiono a sinistra di un blocco per spostarlo su o giu', Alt+clic per
# aprire quel punto in VS Code. Ctrl+C qui chiude tutto.

param([string]$Pagina)

$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

$pagine = Get-ChildItem sorgenti -Filter *.html |
    Where-Object { $_.Name -notlike 'lab-*' -and $_.Name -notlike '_*' } | Sort-Object Name

if (-not $Pagina) {
    Write-Host "`nQuale pagina vuoi modificare?`n" -ForegroundColor Cyan
    $pagine | ForEach-Object { Write-Host ("  " + $_.BaseName) }
    Write-Host ""
    $Pagina = Read-Host "nome o parte del nome"
}

$scelta = $pagine | Where-Object { $_.BaseName -like "*$Pagina*" }
if (-not $scelta) { Write-Host "nessuna pagina contiene '$Pagina'" -ForegroundColor Red; exit 1 }
if ($scelta.Count -gt 1) {
    Write-Host "'$Pagina' corrisponde a piu' pagine:" -ForegroundColor Yellow
    $scelta | ForEach-Object { Write-Host ("  " + $_.BaseName) }
    exit 1
}

Write-Host "`napro $($scelta.Name) — chiudi con Ctrl+C`n" -ForegroundColor Cyan
& .venv\Scripts\python.exe tools\edit_server.py $scelta.Name
