# PowerShell script to fix Arsenal corruption

$errorActionPreference = 'Stop'

$files = @(
    'C:\Users\mateu\OneDrive\Documentos\pxg check\src\index.html',
    'C:\Users\mateu\OneDrive\Documentos\pxg check\index.html'
)

$telemetria_end = '<span class="text-[10px] font-black text-amber-400 uppercase tracking-widest block">Telemetria Financeira</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Painel de fluxo de caixa que compila matematicamente os lucros líquidos diários, semanais e mensais de cada personagem.</p>

                            </div>

                        </li>'

$tactics_f2p_start = '<li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">💡</span>

                            <div>

                                <span class="text-[10px] font-black text-cyan-400 uppercase tracking-widest block">Táticas F2P (Anti-Inflação)</span>'

$replacement = '<span class="text-[10px] font-black text-amber-400 uppercase tracking-widest block">Telemetria Financeira</span>

                                <p class="text-[10px] text-slate-400 font-medium mt-0.5 leading-snug">Painel de fluxo de caixa que compila matematicamente os lucros líquidos diários, semanais e mensais de cada personagem.</p>

                            </div>

                        </li>

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

                        <li class="bg-slate-950 rounded-xl p-3 border border-slate-800 flex items-start gap-3">

                            <span class="text-lg">💡</span>

                            <div>

                                <span class="text-[10px] font-black text-cyan-400 uppercase tracking-widest block">Táticas F2P (Anti-Inflação)</span>'

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "Processing $file"
        try {
            # Read with UTF-8 encoding
            $content = [System.IO.File]::ReadAllText($file, [System.Text.Encoding]::UTF8)
            
            # Find the index position where we need to replace
            $telemetria_idx = $content.IndexOf($telemetria_end)
            if ($telemetria_idx -ge 0) {
                $tactics_idx = $content.IndexOf($tactics_f2p_start, $telemetria_idx)
                if ($tactics_idx -ge 0) {
                    Write-Host "Found both landmarks, performing replacement"
                    # Replace between the two landmarks
                    $before = $content.Substring(0, $telemetria_idx + $telemetria_end.Length)
                    $after = $content.Substring($tactics_idx)
                    $new_content = $before + "`r`r`r`                        " + $replacement
                    
                    # Write back
                    [System.IO.File]::WriteAllText($file, $new_content, [System.Text.Encoding]::UTF8)
                    Write-Host "Fixed $file"
                } else {
                    Write-Host "Could not find Táticas F2P landmark"
                }
            } else {
                Write-Host "Could not find Telemetria landmark"
            }
        } catch {
            Write-Host "Error: $_"
        }
    } else {
        Write-Host "File not found: $file"
    }
}

Write-Host "Done"
