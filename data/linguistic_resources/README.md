# Recursos linguísticos

Os dados de referência do dicionário estão organizados em:

- `data/dictionary.json`: entradas-base e ligações entre Kimbundu, Kikongo e português.
- `data/kimbundu_archive/`: arquivo de acepções Kimbundu dividido em lotes de dez registos.
- `data/umbundu_archive/`: lotes de vocabulário Umbundu com referências às fontes.

O `LocalDictionaryProvider` carrega estes ficheiros para pesquisa e tradução lexical. Na inicialização, a aplicação importa as entradas para SQLite sem duplicar registos já existentes. As bases de dados anteriores recebem automaticamente as colunas Kikongo e Umbundu quando necessário.

As entradas importadas permanecem `unverified` até serem revistas por falantes da língua ou especialistas. As referências indicam a fonte consultada; não significam validação contemporânea nem equivalência contextual para frases completas.

O arquivo Kimbundu inclui entradas do Arquivo Kimbundu, com referências individuais. O vocabulário Umbundu inicial foi consultado no Mundumbundu e mantém links para as páginas temáticas ou de verbete correspondentes.
