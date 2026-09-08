# Recriar os especialistas em outros sistemas

Este kit permite recriar os seis especialistas usando instruções em texto e a base deste repositório. Não depende de um modelo específico. O que é transferido é o papel analítico, os protocolos, as memórias revisadas e o acesso às evidências — não os pesos do modelo nem o histórico privado das conversas.

## Comece por um banco

| Especialista | Instruções para configurar o agente | Conhecimento para anexar |
|---|---|---|
| Banco do Brasil | [instructions.md](agents/Banco_do_Brasil/instructions.md) | [knowledge.md](agents/Banco_do_Brasil/knowledge.md) |
| Bradesco | [instructions.md](agents/Bradesco/instructions.md) | [knowledge.md](agents/Bradesco/knowledge.md) |
| BTG Pactual | [instructions.md](agents/BTG_Pactual/instructions.md) | [knowledge.md](agents/BTG_Pactual/knowledge.md) |
| Caixa | [instructions.md](agents/Caixa/instructions.md) | [knowledge.md](agents/Caixa/knowledge.md) |
| Itaú Unibanco | [instructions.md](agents/Itau/instructions.md) | [knowledge.md](agents/Itau/knowledge.md) |
| Santander Brasil | [instructions.md](agents/Santander/instructions.md) | [knowledge.md](agents/Santander/knowledge.md) |

1. Crie um agente ou uma conversa dedicada ao banco no sistema escolhido.
2. Coloque o conteúdo de `instructions.md` no campo de instruções. Se o campo for pequeno, anexe o arquivo integral e use a mensagem inicial abaixo. Isso depende de o sistema realmente ler anexos; valide antes de confiar.
3. Anexe `knowledge.md`. Para conferir números ou ampliar análises, conecte o clone do repositório ou anexe também as fontes primárias relevantes.
4. Use os [casos de validação](VALIDACAO.md) antes de aceitar a configuração como pronta.

Mensagem inicial reutilizável (substitua o nome do banco):

> Atue como o especialista em [BANCO] definido no arquivo instructions.md anexado. Leia também knowledge.md. Primeiro informe quais arquivos conseguiu acessar, o último trimestre revisado e as lacunas de cobertura. Depois responda às minhas perguntas seguindo o protocolo de evidências. Se não puder abrir os documentos originais, deixe essa limitação explícita e não alegue verificação independente. Responda em português.

## Escolha a forma de uso

| Ambiente | Como conectar | O que permite |
|---|---|---|
| Chat com anexos | Instruções + conhecimento + fontes selecionadas | Trabalhar sobre os arquivos efetivamente anexados |
| IDE com assistente | Abrir o clone e carregar as instruções do banco | Consultar fontes locais e, se autorizado, salvar novas memórias |
| Sistema de agentes com API | Usar as instruções como configuração e implementar recuperação documental | Busca por banco/período e memória versionada sob controle do aplicativo |

Um link público do GitHub não garante que o sistema baixe arquivos, percorra pastas ou leia Git LFS. Cada ambiente tem limites próprios de contexto, anexos e ferramentas. Nenhum pacote deste kit instala extensões ou configura uma conta externa automaticamente.

## Documentos do kit

- [Integração com chats, IDEs e APIs](INTEGRACAO.md): execução local, contrato de busca e limites.
- [Mapa da base de conhecimento](MAPA_DA_BASE.md): onde encontrar cada tipo de evidência.
- [Operação e atualização](OPERACAO.md): como manter o conhecimento consistente entre modelos.
- [Validação dos agentes](VALIDACAO.md): perguntas, resultados esperados e critérios de aceitação.
- [Coordenador de comparação](COORDENADOR.md): instruções opcionais para consolidar os seis bancos.
- [Manifesto dos pacotes](manifest.json): identificadores, arquivos de origem e hashes.

Snapshot inicial: **08/09/2026**, trimestre revisado **2T26**. Os seis guias completos ainda não foram produzidos. As memórias dos calls são leituras temáticas; a Caixa tem cinco períodos anteriores a 2T26 sem transcrição recuperada. Não confunda a configuração pronta com validação analítica em todos os modelos.
