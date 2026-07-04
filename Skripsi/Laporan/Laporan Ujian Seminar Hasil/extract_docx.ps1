Add-Type -AssemblyName 'System.IO.Compression.FileSystem'
$docxPath = Join-Path $PSScriptRoot 'Draft Laporan Ujian Seminar Hasil_Fauzi Noorsyabani_227007042.docx'
$zip = [System.IO.Compression.ZipFile]::OpenRead($docxPath)
$entry = $zip.Entries | Where-Object { $_.FullName -eq 'word/document.xml' }
$stream = $entry.Open()
$reader = New-Object System.IO.StreamReader($stream)
$xml = [xml]$reader.ReadToEnd()
$reader.Close()
$stream.Close()
$zip.Dispose()

$ns = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
$ns.AddNamespace('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')

$paragraphs = $xml.SelectNodes('//w:p', $ns)
$lineNum = 0
foreach($p in $paragraphs) {
    $texts = $p.SelectNodes('.//w:t', $ns)
    $line = ($texts | ForEach-Object { $_.'#text' }) -join ''
    $lineNum++
    Write-Output "${lineNum}: $line"
}
