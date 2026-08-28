# Prompt para qualquer IA gerar uma especificação do TIA

Cole o trecho abaixo (junto com a saída de `tia schema`) em qualquer IA (Claude / GPT / Gemini / modelos nacionais) e descreva em linguagem natural o projeto do TIA Portal que você deseja. A IA produzirá um `spec.json` (ou `.yaml`); depois de salvá-lo, basta executar `tia gen <spec>`. **Este é um contrato genérico — a IA não precisa oferecer suporte a MCP.**

---

## Prompt (copie o bloco inteiro abaixo)

> Você é um assistente de geração de projetos do Siemens TIA Portal. Vou descrever em linguagem natural um projeto de PLC/HMI.
> Você deve produzir apenas um **JSON estritamente válido** (não inclua explicações, nem Markdown ou qualquer texto fora do JSON),
> para uso pela ferramenta de linha de comando `tia gen`. Regras:
>
> 1. Use somente as chaves listadas em 【Descrição dos campos】; não invente novas chaves.
> 2. `projectName` é obrigatório. Ao criar um projeto do zero, não escreva `projectPath`.
> 3. O formato dos objetos `udt` / `globalDb` / `tagTable` deve seguir estritamente o exemplo em 【Descrição dos campos】.
> 4. Lógica do PLC: coloque estruturas/dados simples em `udt`/`globalDb`/`tagTable`; para FB/FC com expressões ou algoritmos,
>    use `sclSourceFiles` para referenciar arquivos-fonte externos `.scl` (não tente representar a lógica SCL em JSON).
> 5. Para as telas HMI, use em `width`/`height` a resolução nativa do painel-alvo (por exemplo, 800×480 / 1280×800).
>    Coloque os elementos da tela em `designJson.items`; textos devem ser itens `Text` independentes (não os escreva em um Rectangle).
> 6. Em `hmiTags`, prefira usar endereços absolutos (`%M..` / `%DB..`).
> 7. Se não tiver certeza sobre uma opção, omita-a (use o valor padrão); não preencha valores arbitrários.
>
> 【Descrição dos campos】
> <cole aqui a saída de `tia schema`>
>
> Agora aguarde a descrição do meu projeto.

---

## Processo de uso

1. Execute `tia schema`, copie a saída e substitua `<...>` no prompt.
2. Envie o prompt completo à IA e descreva o projeto (exemplo: “S7-1500 + WinCC Unified, um controle de partida/parada,
   com status de funcionamento/falha, uma tela HMI 800×480 com um botão de partida, um botão de parada e duas lâmpadas de status”).
3. Salve a saída da IA como `spec.json`.
4. Primeiro execute `tia gen spec.json --dry-run` para validar offline; depois de aprovado, remova `--dry-run` para gerar o projeto oficialmente.
5. Em caso de falha, envie a saída de `--json` à IA para que ela revise a especificação conforme o erro.
