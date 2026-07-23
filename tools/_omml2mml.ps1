# Extract word/document.xml from the ch2 docx and transform OMML -> MathML with Microsoft's OMML2MML.XSL
Add-Type -AssemblyName System.IO.Compression.FileSystem
$xsl = 'C:\Program Files\Microsoft Office\root\Office16\OMML2MML.XSL'
$docx = (Resolve-Path 'originale-docx\da-docx-originale\2. Esperimenti di Stern-Gerlach in cascata\Esperimenti di Stern-Gerlach in cascata.docx').Path
$zip = [IO.Compression.ZipFile]::OpenRead($docx)
$e = $zip.Entries | Where-Object { $_.FullName -eq 'word/document.xml' }
$sr = New-Object IO.StreamReader($e.Open())
$doc = $sr.ReadToEnd(); $sr.Close(); $zip.Dispose()
[IO.File]::WriteAllText((Join-Path (Get-Location) 'build\ch2_document.xml'), $doc, [Text.UTF8Encoding]::new($false))

$settings = New-Object System.Xml.Xsl.XsltSettings($true, $true)
$xslt = New-Object System.Xml.Xsl.XslCompiledTransform
$xslt.Load($xsl, $settings, (New-Object System.Xml.XmlUrlResolver))
$xslt.Transform((Join-Path (Get-Location) 'build\ch2_document.xml'), (Join-Path (Get-Location) 'build\ch2_omml2mml.xml'))

$out = [IO.File]::ReadAllText((Join-Path (Get-Location) 'build\ch2_omml2mml.xml'))
Write-Output ("math count: " + ([regex]::Matches($out,'<(mml:)?math\b')).Count)
Write-Output ("mtable count: " + ([regex]::Matches($out,'<(mml:)?mtable\b')).Count)
