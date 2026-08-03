# Modelo Universal de Controladoria - ORIGINAL vs PROCESSADO

## 📋 MODELO UNIVERSAL DO ORIGINAL (CSV de Banco)

Cada banco envia um CSV com formatação nativa. Não há padrão, mas todos têm **informações essenciais**:

### Identificadores (OBRIGATÓRIOS - sempre presentes)
| Campo | Descrição | Exemplo DIGIO |
|-------|-----------|-------|
| Proposta/Operação | ID único da transação | 404223821 |
| Data | Data da operação ou crédito | 01/07/2026 |

### Valores (CRÍTICOS - comissão paga)
| Campo | Descrição | Exemplo DIGIO |
|-------|-----------|-------|
| Comissão | **VALOR PAGO** (o que o banco confirma pagar) | 1854.02 |
| Base de Cálculo | Valor base para cálculo | 30900.30 |
| Valor Bruto | Valor liberado ou total | 30900.30 |

### Status
| Campo | Descrição | Exemplo DIGIO |
|-------|-----------|-------|
| Situação/Status | "Paga", "Pendente", etc | Paga |
| Tipo Comissão | "Própria", "Rateio", etc | Própria |

### Opcional (presentes em alguns bancos)
| Campo | Descrição |
|-------|-----------|
| Cliente | Nome/CPF do cliente |
| Produto | Tipo de operação |
| Parcelas | Número de parcelas |
| Taxa/Juros | Taxa da operação |

---

## 🔄 MAPEAMENTO: ORIGINAL → PROCESSADO

### Original DIGIO (CSV, 29 colunas)
```
Tp. Lnc | Tipo | Tp.Oper | Oper. | Prop. | Data Base | Data Vcto | ...
       |      |         |       |       |           |           |
       V      V         V       V       V           V           V
```

**↓ TRANSFORMAÇÃO ↓**

### Processado DIGIO (XLSX, 36 colunas - modelo padrão)
```
NUM_BANCO | NOM_BANCO | NUM_PROPOSTA | DAT_CREDITO | VAL_COMISSAO | ...
    335   | BANCO DIG |  404223821   |  01/07/2026 |    1854.02   | ...
```

### Tabela de Mapeamento Completo

| ORIGINAL (CSV DIGIO) | PROCESSADO (XLSX) | Tipo | Notas |
|---|---|---|---|
| Prop. | NUM_PROPOSTA | ID | Identificador único |
| Oper. | NUM_CONTRATO | ID | Contrato |
| Data Base / Dt. Pgto Cmss. | DAT_CREDITO | Data | Quando foi creditado |
| **Valor Comiss** | **VAL_COMISSAO** | Valor | **O valor PAGO** |
| Base de Cálculo | VAL_BASE_COMISSAO | Valor | Base para cálculo |
| Vl Bruto Oper | VAL_BRUTO | Valor | Valor bruto |
| % da Comissão | PCL_COMISSAO | % | Percentual |
| Tipo de Comiss. | DSC_TIPO_COMISSAO | Tipo | Própria, Rateio, etc |
| Tipo de Comiss. | TIPO_COMISSAO_BANCO | Tipo | Confirma tipo |
| Comissionado | (ignorado) | - | Não mapeado |
| PROMOTORA | (ignorado) | - | Não mapeado |
| Empregador | (ignorado) | - | Não mapeado |
| Sit. Pgto | DSC_SITUACAO_BANCO | Status | Paga, Pendente |
| Dt. Cadastro | DAT_CTR_INCLUSAO | Data | Data de inclusão |

---

## 🎯 DETECÇÃO AUTOMÁTICA (para 40+ bancos com formatos diferentes)

Como cada banco pode nomear as colunas diferente, use **busca por padrão**:

### Coluna COMISSÃO (crítica)
**Procura por**: 
- Nome contém "comiss" (case-insensitive)
- Valores são números positivos > 0
- Total da coluna bate com somas esperadas

**Alternativas**: "commission", "incentivo", "fee"

### Coluna DATA
**Procura por**:
- Nome contém "data", "date", "dt.", "data_"
- Valores são datas (formato DD/MM/YYYY, YYYY-MM-DD, etc)
- Agrupar por mês para validar

**Alternativas**: "data pagamento", "data credito", "dt. pgto"

### Coluna PROPOSTA (ID único)
**Procura por**:
- Nome contém "prop", "operação", "oper", "id", "numero"
- Valores são números inteiros
- Cada linha tem valor diferente (sem duplicatas em massa)

**Alternativas**: "contract", "operation", "proposal"

---

## ✅ Validação Pós-Transformação

Após ler CSV original e mapear para o modelo PROCESSADO:

1. **Total de Comissão** deve bater
   - Soma coluna "Valor Comiss" do CSV = Soma VAL_COMISSAO do XLSX

2. **Contagem de linhas** deve bater
   - Linhas no CSV = Linhas no XLSX

3. **Sem linhas duplicadas**
   - Cada NUM_PROPOSTA aparece 1x

4. **Valores positivos**
   - VAL_COMISSAO > 0 (nenhum negativo)

---

## 🔧 Fluxo de Normalização

```
CSV Original (40+ formatos)
    ↓
Detectar colunas (automático)
    ↓
Mapear para colunas padrão
    ↓
Validar (soma, duplicatas, tipos)
    ↓
XLSX Processado (padrão único)
    ↓
Armazenar em SQLite / comparar com PREVISTO
```

