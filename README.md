# Comenda Renato Frota Rodrigues de Azevedo

Site de homenagem do Rotary Club de Volta Redonda, com uma home e 29 páginas personalizadas para associados. A entrada tem um envelope que abre ao tocar na tela. O site inclui a biografia de Renato, duas fotografias e o link de aquisição da peça comemorativa.

## Visualização

Abra `comenda-site/dist/index.html` no navegador ou sirva a pasta:

```sh
python -m http.server 8000 --directory comenda-site/dist
```

Acesse `http://localhost:8000/`. As páginas individuais usam as iniciais de todas as palavras do nome, como `/aef/`. A home não contém atalhos para elas.

## Atualização das páginas

O conteúdo base fica em `comenda-site/dist/index.html`; estilos e comportamento são compartilhados por todas as páginas. Os nomes e tratamentos ficam em `comenda-site/associados.json`.

Depois de alterar a home ou a lista de associados, execute:

```sh
python comenda-site/gerar-paginas.py
```

O gerador atualiza as páginas individuais e a relação administrativa `comenda-site/enderecos-associados.csv` sem modificar a home.

## Hospedagem

O site é estático e não precisa de compilação. Configure a pasta de publicação como **`comenda-site/dist`**, incluindo suas subpastas. Enviar o código ao GitHub não publica automaticamente o site.

### Vercel

Use a raiz do repositório como **Root Directory** (campo vazio ou `./`) e o preset **Other**. O arquivo `vercel.json` define a saída como `comenda-site/dist` e dispensa instalação e compilação. Não combine essa configuração com Root Directory igual a `comenda-site/dist`.

Depois de corrigir o Root Directory, faça um novo deploy da branch `main`. A home estará em `/` e as páginas dos associados em `/aef/`, `/bb/` etc.
