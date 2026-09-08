# Integração em outros ambientes

## Chat ou construtor de agentes

Use os dois documentos do banco listados no [início](README.md). Dê prioridade às instruções no campo próprio da plataforma; se só houver anexos, peça explicitamente a leitura dos dois arquivos. Não cole todos os bancos em uma única configuração de especialista.

Para uma pergunta sobre números, anexe o release/demonstração correspondente, a metodologia e as tabelas necessárias. O conhecimento exportado oferece contexto, mas não substitui documentos primários. Se o sistema não tiver busca nem leitura de arquivos, ele não conseguirá recuperar novas evidências sozinho. Quando o contexto não comportar tudo, selecione banco, período e tema; não corte avisos de comparabilidade ou referências para economizar espaço.

## IDE com acesso a arquivos

Instale Git e Git LFS e execute num terminal:

```sh
git clone https://github.com/franciscoljr/analise-resultados-bancos.git
cd analise-resultados-bancos
git lfs install
git lfs pull
python3 -m venv .venv
```

Ative o ambiente: `source .venv/bin/activate` em macOS/Linux ou `.venv\Scripts\Activate.ps1` no PowerShell. Em seguida:

```sh
python -m pip install -r requirements.txt
```

Abra a pasta clonada na IDE. Carregue `portability/agents/<BANK_ID>/instructions.md` usando o mecanismo de instruções disponível ou peça sua leitura no início da conversa. Os caminhos do kit são relativos à raiz do clone; `REPO_ROOT` significa essa raiz, não uma variável que o modelo já conhece.

Exemplo para Itaú, executado na raiz:

```sh
python scripts/specialist_evidence.py pack --bank Itau
python scripts/specialist_evidence.py index --bank Itau --kind calls
python scripts/specialist_evidence.py search --bank Itau --kind calls --period 2T26 --query "margem captação provisão" --limit 8
```

`pack` grava um inventário; `index` grava o índice local; `search` consulta esse índice. São auxiliares locais existentes, não ferramentas automaticamente registradas no modelo. Só permita execução se o ambiente disponibilizar terminal e houver autorização para a operação. A busca é lexical; use termos ingleses para calls em inglês. Ausência de resultado não prova ausência de informação.

Arquivos iniciados por `version https://git-lfs.github.com/spec/v1` são ponteiros LFS, não o documento original: conclua o download antes de tentar lê-los. As transcrições já existentes dispensam instalar o ambiente de transcrição de mídia. Alguns scripts antigos de mídia/instalação têm caminhos locais; este kit não os torna multiplataforma.

## Aplicativo com API e recuperação documental

O manifesto é um contrato de dados deste projeto, não um formato nativo importável por qualquer fornecedor. O desenvolvedor precisa mapear `instructions` para o campo de instruções do modelo e carregar `knowledge` como contexto. Implemente os adaptadores de leitura/busca na aplicação escolhida; não suponha que os nomes abaixo já sejam ferramentas disponíveis.

Contrato sugerido:

| Operação a implementar | Entrada | Resultado necessário |
|---|---|---|
| `get_bank_context` | Identificador do banco | Memórias atuais, cobertura, período e caminhos de origem |
| `search_evidence` | Banco obrigatório; tema, período, tipo e limite | Trechos com banco, período, caminho, URL, hash e localizador |
| `read_evidence` | Caminho do inventário e página/trecho | Conteúdo e contexto adjacente, mantendo tabelas/cabeçalhos |
| `save_review` | Banco, execução datada, conteúdo e evidências | Arquivos versionados; confirmação explícita de gravação |

Um adaptador pode aproveitar a saída JSON de `specialist_evidence.py`. Não monte comandos de shell por concatenação de entradas do modelo; use argumentos estruturados e valide banco, limites e caminhos dentro do clone. O helper não é um servidor MCP nem uma API remota e não interpreta tabelas ou valida afirmações.

Para busca semântica, indexe documentos por banco e mantenha metadados de período, versão, unidade, tipo de fonte, hash, página/célula/timestamp e status de revisão. Filtre o banco antes da recuperação e mantenha versões conflitantes identificáveis. Não indexe quarentena como evidência válida. Guarde cabeçalhos e notas com tabelas; nunca invente páginas para fragmentos de texto. PDF que exigir conferência visual deve continuar acessível.

Memórias analíticas e documentos primários devem ter tipos distintos no índice: uma resposta anterior não conta como confirmação independente. Defina permissões de escrita separadamente da leitura. O repositório público pode ser lido sem uma chave pessoal; publicação de alterações requer credencial e autorização de quem mantém o projeto.

## Instrução de projeto para uma IDE

Texto sugerido para o campo de regras do projeto, adaptando apenas o identificador:

> Neste projeto, atue conforme portability/agents/Itau/instructions.md. Leia portability/agents/Itau/knowledge.md e os ponteiros atuais de specialists/knowledge/Itau/. Use caminhos relativos à raiz. Antes de citar um número decisivo, abra a fonte e preserve período, unidade, perímetro e localizador. Se um arquivo for ponteiro LFS ou não estiver acessível, informe a lacuna. Não publique alterações nem altere outros bancos sem solicitação.

O nome e o formato do arquivo de regras dependem da IDE; este documento não cria regras globais nem sobrescreve instruções existentes.
