# Biblioteca de instruções SCL (referência neutra)

Este arquivo reúne sintaxes e templates de instruções comuns em SCL para S7-1200 / S7-1500, facilitando a conversão para a DSL de `PlcBuildAndImport(kind=fc|fb)` ou a escrita direta em arquivos de fonte externa `.scl`, para importação por `ImportPlcExternalSource` + `GenerateBlocksFromExternalSource`.

Todos os exemplos usam sintaxe genérica e **não dependem de nenhum processo ou nome de equipamento específico**. Ao copiar para um projeto real, ajuste os nomes das variáveis e as faixas de dados conforme necessário.

## 1. Expressões básicas e fluxo de controle

```scl
// Atribuição e operações
#Out := #A + #B - #C;
#Pct := 100.0 * #Value / #Range;

// Condição
IF #Enable AND NOT #Fault THEN
    #Run := TRUE;
ELSIF #Pause THEN
    #Run := FALSE;
ELSE
    #Run := FALSE;
END_IF;

// Múltiplas ramificações
CASE #Mode OF
    0:  #SP := 0.0;
    1:  #SP := #SP_Manual;
    2:  #SP := #SP_Auto;
ELSE
    #SP := 0.0;
END_CASE;

// Loop
FOR #i := 0 TO 9 DO
    #Sum := #Sum + #Array[#i];
END_FOR;

// Enquanto a condição for verdadeira
WHILE #Counter < #Preset DO
    #Counter := #Counter + 1;
END_WHILE;
```

## 2. Conversão de tipos e escalonamento

| Uso | Instrução |
|---|---|
| Int ↔ Real | `INT_TO_REAL`, `REAL_TO_INT` |
| DInt ↔ Real | `DINT_TO_REAL`, `REAL_TO_DINT` |
| Normalizar para 0–1 | `NORM_X(MIN, VALUE, MAX)` |
| Desnormalizar para unidade de engenharia | `SCALE_X(MIN, NORM, MAX)` |
| Limitação | `LIMIT(MN, IN, MX)` |
| Valor absoluto | `ABS(...)` |

```scl
// Escalonamento analógico (0–27648 → 0–100.0)
#Norm   := NORM_X(MIN := 0,    VALUE := #RawAI, MAX := 27648);
#Engineering := SCALE_X(MIN := 0.0, VALUE := #Norm,  MAX := 100.0);
#Limited := LIMIT(MN := 0.0, IN := #Engineering, MX := 100.0);
```

## 3. Detecção de flancos

```scl
// Instanciação de R_TRIG / F_TRIG (declarada na área Static para preservar a instância)
#RisingStart(CLK := #Cmd_Start);
IF #RisingStart.Q THEN
    #PulseCount := #PulseCount + 1;
END_IF;
```

## 4. Temporizadores (IEC)

```scl
// TON: retardo na energização (instância no Static do FB ou em um DB independente)
#Ton1(IN := #Cmd_Run, PT := T#3S);
#Delayed := #Ton1.Q;

// TOF: retardo na desenergização
#Tof1(IN := #Cmd_Run, PT := T#1S);

// TP: pulso único
#Tp1(IN := #Trigger, PT := T#500MS);
```

> Não é possível criar instâncias de temporizadores IEC dentro de um FC (especialmente em F-CPU); coloque a instância na seção **FB Static** ou em um **DB global**.

## 5. Contadores (IEC)

```scl
#Ctu1(CU := #Cmd_Inc, R := #Cmd_Clear, PV := #Preset);
#Value := #Ctu1.CV;
#Done  := #Ctu1.Q;
```

## 6. Padrão de chamada do PID_Compact (somente interface de parâmetros)

```scl
"PID_Compact_1"(
    Setpoint  := #SP,
    Input     := #PV,
    Output    => #OUT,
    ManualEnable := #Mode_Manual,
    ManualValue  := #ManOut,
    Reset     := #Cmd_Reset
);
```

Descrição dos parâmetros (seleção):
- `Setpoint` / `Input` são obrigatórios e têm tipo `Real`;
- `Output` é a saída calculada;
- com `ManualEnable=TRUE`, o modo manual é executado;
- `Reset=TRUE` muda para o estado “não ativado”;
- leia os demais parâmetros (`Mode`, `PIDStatus`, `Error`) conforme necessário.

## 7. Comparação segura e banda morta

```scl
// Comparação com banda morta
#Diff := ABS(#SP - #PV);
IF #Diff <= #Deadband THEN
    #Reached := TRUE;
ELSE
    #Reached := FALSE;
END_IF;

// Comparação de três estados
IF #PV > #HighLimit THEN
    #Level := 2;
ELSIF #PV >= #LowLimit THEN
    #Level := 1;
ELSE
    #Level := 0;
END_IF;
```

## 8. Rampa / limitação de velocidade (template genérico)

```scl
// Variação máxima por ciclo (influenciada pelo tempo de varredura)
IF #Target > #Current + #RampUp THEN
    #Current := #Current + #RampUp;
ELSIF #Target < #Current - #RampDown THEN
    #Current := #Current - #RampDown;
ELSE
    #Current := #Target;
END_IF;
```

## 9. Arrays e estilo FOR-EACH

```scl
// Soma
#Sum := 0.0;
FOR #i := 0 TO 9 DO
    #Sum := #Sum + #Buffer[#i];
END_FOR;
#Avg := #Sum / 10.0;

// Maior valor
#Max := #Buffer[0];
FOR #i := 1 TO 9 DO
    IF #Buffer[#i] > #Max THEN
        #Max := #Buffer[#i];
    END_IF;
END_FOR;
```

## 10. Referência a UDT

```scl
// Supondo que UDT_BasicStatus contenha Active/Error/Setpoint/Actual
#Item.Active   := #Run;
#Item.Error    := #Fault;
#Item.Setpoint := #SP;
#Item.Actual   := #PV;
```

## 11. Concatenação de strings (suporte somente em 1500/alguns 1200)

```scl
#Msg := CONCAT(IN1 := 'STEP=', IN2 := DINT_TO_STRING(#Step));
```

## 12. Códigos de erro e log (padrão recomendado)

```scl
IF #SensorErr THEN
    #ErrorCode := 1001;
    #Status    := 'Sensor lost';
ELSIF #DriveErr THEN
    #ErrorCode := 1002;
    #Status    := 'Drive fault';
ELSE
    #ErrorCode := 0;
    #Status    := 'OK';
END_IF;
```

## 13. Compatibilidade com a DSL (`PlcBuildAndImport(kind=fc|fb)`)

A DSL oferece suporte direto a `assignment`, `if/elsif/else/endif`, `line`, `token` e `literal`.
Para sintaxes **não suportadas** (`FOR`/`WHILE`/`CASE`/`REPEAT`/`EXIT`/`CONTINUE`/`RETURN`), use:

- **Fonte SCL externa**: grave o `.scl` completo no disco (UTF-8 + BOM) e use `ImportPlcExternalSource`, seguido de `GenerateBlocksFromExternalSource`;
- ou edite no TIA, use `ExportBlock` e depois importe com `ImportBlock`.
