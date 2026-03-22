#Requires -Version 5.0
param(
    [string]$FilePath = 'c:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html'
)

Write-Host "Reading file: $FilePath"

# Read file as text with error handling
$content = [System.IO.File]::ReadAllText($FilePath, [System.Text.Encoding]::UTF8)

# Check if we have the content we need
if ($content -notmatch 'Rastreio de Rainbow Orbs') {
    Write-Host "ERROR: File does not contain expected text"
    exit 1
}

Write-Host "Found 'Rastreio de Rainbow Orbs' in file"

# Count occurrences
$count = ($content | Select-String -Pattern 'Rastreio de Rainbow Orbs' -AllMatches).Matches.Count
Write-Host "Found $count instances of 'Rastreio de Rainbow Orbs'"

# Use IndexOf to find the positions
$idx1 = $content.IndexOf('Rastreio de Rainbow Orbs')
$idx2 = $content.IndexOf('Rastreio de Rainbow Orbs', $idx1 + 1)

if ($idx1 -lt 0 -or $idx2 -lt 0) {
    Write-Host "ERROR: Could not find both instances"
    exit 1
}

Write-Host "First instance at position: $idx1"
Write-Host "Second instance at position: $idx2"

# Show context around both
Write-Host "`nContext around first instance (200 chars before and after):"
$context1 = $content.Substring([Math]::Max(0, $idx1-100), 200)
Write-Host $context1

Write-Host "`nContext around second instance (200 chars before and after):"
$context2 = $content.Substring([Math]::Max(0, $idx2-100), 200)
Write-Host $context2

# Find "Telemetria Financeira" and "Táticas F2P" unique landmarks
$telemetria_idx = $content.IndexOf('Telemetria Financeira')
$f2p_idx = $content.IndexOf('Táticas F2P')

if ($telemetria_idx -lt 0 -or $f2p_idx -lt 0) {
    Write-Host "ERROR: Could not find landmarks"
    exit 1
}

Write-Host "`nTelemetria at: $telemetria_idx"
Write-Host "F2P at: $f2p_idx"

# Find the li blocks
# Go backward from Telemetria to find its opening <li
$li_telemetria_start = $content.LastIndexOf('<li class="bg-slate-950', $telemetria_idx)
$li_telemetria_end = $content.IndexOf('</li>', $telemetria_idx) + 5

# Go backward/forward from F2P to find its li block  
$li_f2p_start = $content.LastIndexOf('<li class="bg-slate-950', $f2p_idx)
$li_f2p_end = $content.IndexOf('</li>', $f2p_idx) + 5

Write-Host "`nTelemetria li: $li_telemetria_start to $li_telemetria_end"
Write-Host "F2P li: $li_f2p_start to $li_f2p_end"

# Extract the Telemetria and F2P items
$telemetria_html = $content.Substring($li_telemetria_start, $li_telemetria_end - $li_telemetria_start)
$f2p_html = $content.Substring($li_f2p_start, $li_f2p_end - $li_f2p_start)

Write-Host "`nTelemetria HTML length: $($telemetria_html.Length)"
Write-Host "F2P HTML length: $($f2p_html.Length)"

# Build the corrected Arsenal section
$newArsenal = @"
$telemetria_html

                        <li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">🔮</span>

                            <div>

                                <span class="text-[10px] font-black text-purple-400 uppercase tracking-widest block">Rastreio de Rainbow Orbs</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Mapeamento interativo das 245 orbs. Otimiza o seu tempo de exploração bloqueando o re-check constante de áreas e coordenadas já visitadas.</p>

                            </div>

                        </li>

                        <li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">🔔</span>

                            <div>

                                <span class="text-[10px] font-black text-rose-400 uppercase tracking-widest block">Despertador Cognitivo</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Estimulação visual (pulsações neon) e áudio dinâmico despachado 5 minutos antes da iniciação de Globais e Poképarks.</p>

                            </div>

                        </li>

                        $f2p_html
"@

# Rebuild the content
$before = $content.Substring(0, $li_telemetria_start)
$after = $content.Substring($li_f2p_end)
$newContent = $before + $newArsenal + $after

# Write back
Write-Host "`nWriting fixed content to file..."
[System.IO.File]::WriteAllText($FilePath, $newContent, [System.Text.Encoding]::UTF8)

Write-Host "SUCCESS! File has been fixed."
Write-Host "Total replacements made in document structure"
