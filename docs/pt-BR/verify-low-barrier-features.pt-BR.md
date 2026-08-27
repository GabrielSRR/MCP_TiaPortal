# Recursos de baixa barreira — status e como verificar

Data do status: 2026-06-16.

## 1. Resolução tolerante de `softwarePath` — IMPLEMENTADA

`GetPlcSoftware` agora usa uma correspondência tolerante quando não encontra o caminho exato:

- aceita diferenças de maiúsculas/minúsculas e espaços ao redor;
- em um projeto com um único PLC, resolve qualquer token para o único PLC;
- uma substring exclusiva, sem diferenciar maiúsculas/minúsculas, é resolvida (por exemplo, `"PLC"` → `"PLC_1"`, `"安全"` → `"安全PLC"`);
- quando ainda não consegue resolver, as ferramentas de listagem (`GetPlcTagTables`, `GetPlcExternalSources`, `GetPlcWatchTables`) terminam o erro com `Available PLC paths: <name1>, <name2>, …`.

**Status da verificação**

- O matcher puro `Guard.MatchPlcName` passou em 16 casos offline determinísticos (PLC único, maiúsculas/minúsculas, espaços, substring exclusiva, ambígua→nenhuma, inexistente→nenhuma). Execute `scripts/Test-MatchPlcName.ps1`.
- A verificação pontual online deve ser feita no **seu MCP conectado**; um processo de teste iniciado a frio pode travar no handshake de conexão/confiança do Openness:

```text
AttachToOpenProject → GetProjectTree                  # anote os nomes reais dos PLCs
GetPlcTagTables(softwarePath="<maiúsculas/espaços/substring>")  # resolve sem erro
GetPlcTagTables(softwarePath="NoSuchPlc")             # erro termina com "Available PLC paths: …"
```

Tudo é somente leitura; nenhuma gravação é realizada.

## 2. Download para CPU V21 — CORRIGIDO (validado em CPU real em 2026-06-17)

`DownloadToPlc` funciona na V21: a conversão foi corrigida (`ConfigurationTargetInterface` é o `IConfiguration`) e o prompt de `StopModules` é tratado (`StopAll`). Validado de ponta a ponta em um S7-1200 real (安全PLC): `state=Success, 0 errors` (parada → download → reinicialização). Consulte SKILL.md §13.
