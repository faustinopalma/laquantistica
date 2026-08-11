# Riconoscimento ottico con il motore incorporato in Windows (Windows.Media.Ocr).
# Va eseguito con Windows PowerShell 5.1: pwsh 7 non ha la proiezione WinRT.
# Uso:  powershell.exe -ExecutionPolicy Bypass -File build\i18n\ocr_windows.ps1

$ErrorActionPreference = 'Stop'
$cartella = Join-Path $PSScriptRoot '..\..\privato\librettouniversitario' | Resolve-Path
$uscita = Join-Path $cartella '_ocr'
New-Item -ItemType Directory -Force -Path $uscita | Out-Null

Add-Type -AssemblyName System.Runtime.WindowsRuntime
$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
  $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and
  $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]

function Attendi($operazione, $tipo) {
  $asTask = $asTaskGeneric.MakeGenericMethod($tipo)
  $task = $asTask.Invoke($null, @($operazione))
  $task.Wait(-1) | Out-Null
  $task.Result
}

[Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics, ContentType = WindowsRuntime] | Out-Null
[Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
[Windows.Globalization.Language, Windows.Globalization, ContentType = WindowsRuntime] | Out-Null

$lingue = [Windows.Media.Ocr.OcrEngine]::AvailableRecognizerLanguages
Write-Output "lingue disponibili per il riconoscimento: $(($lingue | ForEach-Object { $_.LanguageTag }) -join ', ')"

$motore = $null
foreach ($tag in @('it-IT', 'it', 'en-US', 'en-GB')) {
  $l = $lingue | Where-Object { $_.LanguageTag -eq $tag } | Select-Object -First 1
  if ($l) { $motore = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($l); break }
}
if (-not $motore) { $motore = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages() }
if (-not $motore) { throw 'nessun motore di riconoscimento disponibile' }
Write-Output "motore in uso: $($motore.RecognizerLanguage.LanguageTag)"

Get-ChildItem $cartella -File | Where-Object { $_.Extension -match '^\.(jpg|jpeg|png)$' } | ForEach-Object {
  $f = $_
  $file = Attendi ([Windows.Storage.StorageFile]::GetFileFromPathAsync($f.FullName)) ([Windows.Storage.StorageFile])
  $flusso = Attendi ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
  $dec = Attendi ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($flusso)) ([Windows.Graphics.Imaging.BitmapDecoder])
  $bmp = Attendi ($dec.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
  $ris = Attendi ($motore.RecognizeAsync($bmp)) ([Windows.Media.Ocr.OcrResult])

  $righe = @()
  foreach ($r in $ris.Lines) { $righe += $r.Text }
  $dest = Join-Path $uscita ($f.BaseName + '.txt')
  $righe -join "`n" | Set-Content -Path $dest -Encoding UTF8
  Write-Output ("{0,-46} {1,4} righe -> {2}" -f $f.Name, $righe.Count, (Split-Path $dest -Leaf))
  $flusso.Dispose()
}
Write-Output 'fatto'
