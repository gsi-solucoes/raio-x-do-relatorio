# Raio X do Relatório — Concepção da versão 2.0

Conversa com o Galindo · versão 2.0-rascunho · 28/11/2026 · **aguardando portão 1**.
Enquanto o Galindo não aprovar, vale a concepção v1 (`concepcao.md`) e a homologação da versão atual segue normalmente.

Fontes: áudio de 28/11 (`transcricoes/2026-11-28-audio-cerebro.md`), conversa de 28/11 (memória `2026-11-28_b1a62921`),
pesquisa de 26 a 28/11 (`docs/pesquisa/descoberta-de-padroes/`: regras R1–R23, 28 requisitos da tela, testes às cegas),
"Versão 2.0" do POP (F-72).

## 1. A ideia (Galindo, 28/11/2026)
"Criar um script bem inteligente, para ele pensar igual uma inteligência artificial. A ideia é imitar o cérebro."
O Raio X lê qualquer planilha que nunca viu e descreve o que ela é **pensando por partes**, como um cérebro,
usando o que aprendeu. Quanto mais aprende, melhor fica e menos pergunta.

**O script inteiro é a inteligência.** Não há IA de fora: sai o desenho de 27/11 "script = cérebro, IA = neurônio,
porteiro confere". Os neurônios ficam dentro do script e a conferência vira um passo do raciocínio.
Consequência: sai o requisito 6 da tela (botão "Ativar relatórios mais inteligentes", download de ~1 GB, WebGPU) e o
teste do Gemini Nano deixa de decidir algo. A inteligência vale para todo mundo, inclusive no celular, porque é leve.

## 2. As 5 partes do cérebro (todas ligadas)
| # | Parte | O que é |
|---|---|---|
| 1 | **Como ele age** | Recebe o arquivo, olha e **mapeia** cada célula (endereço, linha, coluna, o que está em volta), monta a planilha e faz as perguntas |
| 2 | **Como ele pensa** | Os **mecanismos de identificação** são os **neurônios**: cada um olha uma pista só (cara da célula: valor, data, categoria, texto, código; rótulo ao lado; cabeçalho em cima; repetição; código de categoria; linha do tempo das datas; cruzamento com outros relatórios) e dá um sinal com força. As vizinhas mais perto pesam mais. O cérebro soma os sinais, **confere** se a conclusão bate com as provas (ex.: abertura não vem depois do encerramento; se não bate, pensa de novo) e chega a uma conclusão com **grau de certeza** |
| 3 | **Como ele guarda** | (a) **Carga de fora:** o que aprendeu na sala de aula, que vem pronto dentro do app. (b) **Guarda na hora:** o mapa do arquivo recebido, as conclusões, os sinônimos descobertos e o que o cliente confirmou |
| 4 | **Como ele lembra** | Ao pensar, busca na memória só o que serve para aquela célula ou coluna, nas três fontes: carga de fora, o que guardou no uso e o que está gerando agora no próprio arquivo e nos outros relatórios carregados |
| 5 | **Como ele entrega** | Planilha montada, "Já identifiquei sozinho" (com "corrigir"), "Preciso da sua ajuda" só com as dúvidas, conclusão pronta com a prova curta; depois painel e relatórios |

**Ciclo:** age → lembra → pensa → entrega → guarda. Na próxima vez lembra mais, pensa melhor e pergunta menos.

**Livro de conceitos:** o que é planilha, tipos de célula, tipos de planilha (tabela, ficha, agrupado, cabeçalho
deslocado ou repetido, formulário, título + tabela), ordem natural das datas, código × número × valor (R$).
Fica num arquivo separado, que o script lê antes de pensar. Hoje está espalhado em `analise_manual.md` e no código.

## 3. Memória e aprendizado
- **Para melhorar, enche-se a memória.** O cérebro é construído uma vez. Depois disso, ele melhora porque a memória cresce.
- **Duas fontes de alimentação:**
  1. **Sala de aula (de fora):** script na oficina (`gsi-oficina/sala-de-aula/`) que gera planilhas de todo tipo com
     gabarito; o cérebro resolve, é corrigido e a força de cada neurônio e ligação se ajusta. A matéria nova vira
     neurônio novo. Sai um **arquivo de memória pequeno** (KB a poucos MB), que vai dentro do app.
  2. **No uso (ele mesmo):** cada arquivo e cada confirmação do cliente vira memória naquele aparelho.
- **Lembrança provisória:** o que ele conclui sozinho também é guardado, com peso menor. Vira firme quando é
  conferido (o cliente confirma ou o gabarito bate). Se o cliente corrige, a lembrança perde força.
- **Pista de um tipo totalmente novo** pede um neurônio novo, escrito uma vez. Depois disso, a memória faz o resto.
- A memória fica **no navegador**, com "Apagar o que aprendeu". Começa sem nada do caso de origem.
- **Prova de que aprende (oráculo):** planilhas que ele nunca viu na aula, de ramos diferentes. A cada rodada de aula, a nota
  tem que subir e as perguntas têm que cair. Mantém-se o combinado: o teste mostra o resultado da primeira passada.

## 4. Itens da V2 que entram agora (Galindo, 28/11/2026)
1. **O cérebro** (seções 1 a 3) e a nova tela de colunas (requisitos 1–5 e 7–28 de `requisitos_tela.md`; o 6 sai).
2. **Clientes ou contratos separados:** seletor "Cliente ▾" e "+ Novo cliente", aba de cor própria dentro da paleta,
   relatórios, nome, logo, metas, painel, backup e **memória** próprios.
3. **Histórico de alterações:** a cada carga, guarda campo, valor antigo, valor novo e data; "Exibir histórico" e Excel.
4. **Compartilhar aprendizado com a GSI:** por e-mail para solucaogsi@gmail.com, só configurações e o que aprendeu,
   **nunca os registros**. O app continua sem servidor.
5. **OCR em outros idiomas** (D-63).
6. **Fotos pela câmera, várias de uma vez** (adicionar, retirar, X para fechar).

**Fica para a V3:** a versão Excel para baixar no computador (macro `excel/RaioX_Relatorio.bas`, P-z, D-24, F-49).
O botão do app que gera o arquivo Excel continua.

## 5. O que NÃO quero
- Nada online: sem servidor, sem API, sem IA paga, sem IA de fora. Os arquivos da pessoa não saem do aparelho.
- Nada do caso de origem (nomes, regras, frases) no conhecimento nem na memória que vai no app.
- Aprender palpite como certeza.
- Pergunta que vira teste de lógica: quem calcula é o app; a pessoa só confirma ou corrige (requisito 18).

## 6. Decisões provisórias ⚖️ (conferir no portão 1)
- ⚖️ **Requisito 14 fica:** quando a resposta da pessoa contradiz uma prova forte, o app mostra a prova e pergunta
  "Quer manter mesmo assim?". É um comportamento da tela, não um porteiro.
- ⚖️ A sala de aula é a 3ª bancada da oficina (`gsi-oficina/sala-de-aula/`), ao lado de `simuladores/` e `dubles/`.
- ⚖️ As 23 regras do protótipo são os primeiros neurônios; os limites fixos delas (80%, 95%, 5%) viram pesos aprendidos.

## 7. Próximos passos
1. ✋ Portão 1: Galindo aprova esta concepção.
2. Prova no protótipo, antes da fábrica: cérebro com memória + sala de aula mínima e o teste "pergunta menos na 2ª vez".
3. Especificação (a partir desta concepção e de `requisitos_tela.md`) → ✋ portão 2 → fábrica.
   A V2 entra na linha depois das tarefas atuais da homologação (F-85 a F-89).
