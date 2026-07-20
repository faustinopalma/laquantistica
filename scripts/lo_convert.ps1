param([string]$Fmt = "fodt", [string]$OutDir = "build\fodt", [string[]]$Docs)
$sw = [Diagnostics.Stopwatch]::StartNew()
# LibreOffice ships its own Python; our venv's PYTHON* vars break it ("Could not
# find platform independent libraries"). Clear them for this child process.
$env:PYTHONHOME = $null
$env:PYTHONPATH = $null
$env:PYTHONSTARTUP = $null
$env:PYTHONUTF8 = $null
# soffice.com is the console wrapper that BLOCKS until conversion finishes
# (soffice.exe is a launcher that returns immediately).
$soffice = "C:\Program Files\LibreOffice\program\soffice.com"
$prof = "file:///" + ($PWD.Path -replace '\\', '/') + "/build/louser"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
foreach ($d in $Docs) {
  & $soffice "-env:UserInstallation=$prof" --headless --convert-to $Fmt --outdir $OutDir $d *> $null
  Write-Output ("converted: " + [IO.Path]::GetFileName($d) + " -> " + (Test-Path (Join-Path $OutDir ([IO.Path]::GetFileNameWithoutExtension($d) + "." + ($Fmt -split ':')[0]))))
}
Write-Output ("elapsed: {0:N1}s" -f $sw.Elapsed.TotalSeconds)
