# Operação e atualização

## Memória entre sistemas

Use o repositório como fonte compartilhada. Conversas isoladas não sincronizam memória automaticamente. Uma alteração feita só no chat de outro sistema não chega aos demais agentes.

Para incorporar uma nova análise autorizada:

1. Consulte a versão atual e leia os ponteiros do banco.
2. Revise as fontes usadas e registre período, perímetro, localizador e cálculos.
3. Salve uma execução datada em `specialists/knowledge/<BANK_ID>/runs/<timestamp>/`, seguindo o contrato do guia quando aplicável. Marque resultados parciais e fontes não verificadas.
4. Preserve versões anteriores e explique alterações de conclusão. Só atualize o ponteiro depois da revisão. Para atualizar memórias temáticas, mantenha os campos dos respectivos `latest_calls.json` e `latest_business_mix.json`.
5. Revise e integre a alteração ao repositório. Uma contribuição externa pode ser proposta para revisão; acesso público não concede edição direta.
6. Regenere o kit e recarregue os anexos ou o índice nos sistemas que o utilizam.

Evite dois sistemas escrevendo no mesmo ponteiro simultaneamente; use execuções distintas e resolva a integração na revisão. Não coloque credenciais ou histórico privado de conversas nos documentos públicos.

## Regenerar os pacotes

Na raiz do clone:

```sh
python scripts/export_portable_agents.py
```

O exportador gera os doze documentos dos bancos e o manifesto a partir dos perfis, protocolo, contrato e memórias apontadas. Ele não coleta resultados novos nem produz análise adicional. Uma nova memória de guia em `latest.json` não é incorporada automaticamente por esta primeira versão: inclua esse material explicitamente numa evolução do exportador antes de anunciar que foi exportado.

O manifesto registra hashes dos insumos e o commit que existia ao gerar o pacote. Se houver mudanças locais, os hashes identificam os bytes efetivos; o commit sozinho não comprova esses bytes. A data e o trimestre de snapshot são explícitos no exportador e precisam ser revisados junto com a cobertura ao publicar uma nova versão.

Para novas divulgações, siga o fluxo de atualização do README principal, confira o status e revise as novas fontes antes de renovar conclusões. Um download concluído não implica leitura concluída. Depois de regenerar, execute os casos de validação e registre ambiente, modelo/data e falhas. Não foi configurada atualização recorrente.
