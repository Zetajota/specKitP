param(
    [string]$Remoto = 'origin'
)

$ErrorActionPreference = 'Stop'
$raiz = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path.Replace('\', '/')

function Ejecutar-Git {
    param([string[]]$Argumentos)
    $salida = & git -c "safe.directory=$raiz" @Argumentos
    if ($LASTEXITCODE -ne 0) {
        throw "Git falló al ejecutar: git $($Argumentos -join ' ')"
    }
    return $salida
}

$raizGit = Ejecutar-Git @('rev-parse', '--show-toplevel')
if (-not $raizGit) { throw 'No se encontró un repositorio Git.' }

$rama = (Ejecutar-Git @('branch', '--show-current')).Trim()
if (-not $rama) { throw 'No publiques desde una referencia sin rama.' }

$sinResolver = @(Ejecutar-Git @('diff', '--name-only', '--diff-filter=U'))
if ($sinResolver.Count -gt 0 -and $sinResolver[0]) {
    throw "Hay conflictos sin resolver: $($sinResolver -join ', ')"
}

Ejecutar-Git @('diff', '--check') | Out-Null
Ejecutar-Git @('diff', '--cached', '--check') | Out-Null
$cambios = @(Ejecutar-Git @('status', '--porcelain'))
if ($cambios.Count -gt 0 -and $cambios[0]) {
    throw 'Hay cambios sin commit. Confírmalos antes de publicar.'
}

Ejecutar-Git @('fetch', '--prune', $Remoto) | Out-Null
$referencia = "refs/remotes/$Remoto/$rama"
& git -c "safe.directory=$raiz" show-ref --verify --quiet $referencia
if ($LASTEXITCODE -ne 0) {
    $referencia = "refs/remotes/$Remoto/main"
    & git -c "safe.directory=$raiz" show-ref --verify --quiet $referencia
    if ($LASTEXITCODE -ne 0) {
        throw "No se encontró $Remoto/$rama ni $Remoto/main para comparar."
    }
}

Ejecutar-Git @('merge-base', 'HEAD', $referencia) | Out-Null
$conteos = ((Ejecutar-Git @('rev-list', '--left-right', '--count', "HEAD...$referencia")) -join '').Trim() -split '\s+'
if ($conteos.Count -ne 2) { throw 'No se pudieron interpretar los conteos de Git.' }
$adelante = [int]$conteos[0]
$atras = [int]$conteos[1]
Write-Output "Rama local: $rama; referencia remota: $referencia; adelante: $adelante; atrás: $atras."
if ($atras -gt 0) {
    throw 'El remoto contiene commits ausentes localmente. Integra y resuelve conflictos antes del push.'
}
Write-Output 'Lista para push: sin cambios pendientes ni commits remotos faltantes.'
