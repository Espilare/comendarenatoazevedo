"""Generate member invitations from the current home without changing the home."""
from pathlib import Path
import csv
import html
import json
import re
import unicodedata

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'


def initials(name):
    normalized = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    return ''.join(word[0].lower() for word in normalized.split())


def main():
    members = json.loads((ROOT / 'associados.json').read_text(encoding='utf-8'))
    home = (DIST / 'index.html').read_text(encoding='utf-8')
    routes = [initials(member['nome']) for member in members]
    if len(routes) != len(set(routes)):
        raise ValueError('Iniciais repetidas: definir enderecos distintos antes de gerar.')
    rows = []
    for member, route in zip(members, routes):
        name = html.escape(member['nome'])
        female = member['tratamento'] == 'feminino'
        salutation = 'Prezada companheira,' if female else 'Prezado companheiro,'
        page = home.replace(
            '<title>Uma homenagem à sua trajetória | Rotary Club de Volta Redonda</title>',
            f'<title>{name} | Comenda Renato Azevedo</title>', 1
        )
        page = page.replace('<body>', '<body class="personalized">', 1)
        page = page.replace('</head>', '<meta name="robots" content="noindex, nofollow">\n</head>', 1)
        page = page.replace('COM ESTIMA E RECONHECIMENTO', name, 1)
        old = '<p class="salutation">Prezado companheiro,</p>'
        if old not in page:
            raise ValueError('Saudacao da home mudou; atualizar o gerador.')
        page = page.replace(old, f'<p class="salutation">{salutation}</p><p class="recipient-name">{name}</p>', 1)
        if female:
            page = page.replace('Você foi selecionado para receber a', 'Você foi selecionada para receber a', 1)
        # The shared assets live one directory above each member page.
        page = re.sub(
            r'\b(src|href)="([^"#]+)"',
            lambda match: match[0] if re.match(r'(?:[a-z]+:|/)', match[2], re.I)
            else f'{match[1]}="../{match[2]}"',
            page,
        )
        folder = DIST / route
        folder.mkdir(exist_ok=True)
        (folder / 'index.html').write_text(page, encoding='utf-8')
        rows.append({'Nome': member['nome'], 'Caminho': f'/{route}/', 'Tratamento': member['tratamento']})
    # Administrative list kept outside the published site.
    with (ROOT / 'enderecos-associados.csv').open('w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Nome', 'Caminho', 'Tratamento'], delimiter=';')
        writer.writeheader()
        writer.writerows(rows)
    assert (DIST / 'index.html').read_text(encoding='utf-8') == home
    print(f'{len(rows)} paginas geradas. Home preservada, sem atalhos.')


if __name__ == '__main__':
    main()
