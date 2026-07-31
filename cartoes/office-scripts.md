---
tecnologia: office-scripts
detectar: ["*.osts", "**/Office Scripts/*.ts"]
papeis: [arquiteto, implementador, revisor]
versao: 2026-07-31
---

## Convenções
- Todo script tem uma função `main` cujo primeiro parâmetro é obrigatoriamente `workbook: ExcelScript.Workbook` — é assim que o Excel injeta o workbook ao rodar o script; parâmetros extras (para entrada via Power Automate) vêm depois dele.
- A API do Office Scripts é síncrona (sem `context.sync()`/`load()` como no Office.js de add-in) — não recria esse padrão de proxy/sync à toa.
- Script só roda se estiver salvo no OneDrive/SharePoint (pasta "Office Scripts") ou compartilhado com o workbook; um `.ts` solto fora dali não aparece no Excel.
- Quando o script é chamado por um flow do Power Automate, os parâmetros de entrada e o valor de retorno da `main` só podem ser tipos serializáveis em JSON (string, number, boolean, array, object) — nunca um objeto do próprio `ExcelScript` (`Range`, `Worksheet`) como retorno.

## Armadilhas
- Office Scripts não suporta biblioteca externa nem `import` de pacote — só as APIs do `ExcelScript` e objetos nativos do JavaScript/TypeScript (`Math`, etc.); código que depende de um pacote npm não roda ali.
- O arquivo `.osts` é o formato pronto para importar no Excel; o `.ts` ao lado é só o texto fonte — editar um sem reexportar/sincronizar o outro deixa os dois divergentes.
- Um script auto-contido só enxerga funções definidas no próprio arquivo — não há import entre scripts.

## Checklist de review
- [ ] `main` declara `workbook: ExcelScript.Workbook` como primeiro parâmetro.
- [ ] Nenhum `import` de pacote externo.
- [ ] Parâmetros e retorno usados com Power Automate são tipos simples serializáveis em JSON.
- [ ] Nenhuma dependência de estado deixado por outro script (o script é autocontido).
