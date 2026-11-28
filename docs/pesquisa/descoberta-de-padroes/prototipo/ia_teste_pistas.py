"""Pistas do ia_teste.py sem carregar IA (gerado de ia_teste.py)."""
import os
OPCOES = ['Abertura / pedido', 'Compra / nota', 'Início do serviço', 'Fim do serviço / executado', 'Encerramento / baixa',
          'Previsão / programada', 'Competência / período', 'Nascimento', 'Outra', '?']
SISTEMA = ("Você decide o significado de uma coluna de datas de um relatório. Um programa leu o relatório e te mostra um grupo de "
           "células que são datas. Diga QUAL data é, escolhendo exatamente uma destas opções: " + '; '.join(OPCOES) + ". "
           "Use 'Outra' se for uma data com outro significado e '?' se não der para saber. "
           "Se precisar, peça informação ao programa usando as ferramentas (no máximo 4 pedidos). "
           "No fim, responda SOMENTE com JSON: {\"qual_data\": \"<opção>\", \"confianca\": \"alta|média|baixa\", \"porque\": \"<curto>\"}.")
FERRAMENTAS = [
    {'type': 'function', 'function': {'name': 'exemplos', 'description': 'Mostra mais exemplos de valores do grupo.', 'parameters': {'type': 'object', 'properties': {'grupo': {'type': 'string'}}, 'required': ['grupo']}}},
    {'type': 'function', 'function': {'name': 'vizinhos', 'description': 'Mostra os rótulos/textos que ficam perto deste grupo no relatório (mesma linha ou cabeçalho).', 'parameters': {'type': 'object', 'properties': {'grupo': {'type': 'string'}}, 'required': ['grupo']}}},
    {'type': 'function', 'function': {'name': 'ordem_no_tempo', 'description': 'Compara este grupo de datas com os outros grupos de datas do mesmo registro: quem vem antes e a diferença típica.', 'parameters': {'type': 'object', 'properties': {'grupo': {'type': 'string'}}, 'required': ['grupo']}}},
    {'type': 'function', 'function': {'name': 'arredores', 'description': 'Mostra o que tem antes e depois na mesma linha, e a linha de cima e de baixo, para alguns exemplos do grupo, como está no arquivo.', 'parameters': {'type': 'object', 'properties': {'grupo': {'type': 'string'}}, 'required': ['grupo']}}},
    {'type': 'function', 'function': {'name': 'trecho', 'description': 'Mostra um trecho cru do arquivo (5 linhas) em volta de um exemplo do grupo.', 'parameters': {'type': 'object', 'properties': {'grupo': {'type': 'string'}}, 'required': ['grupo']}}},
    {'type': 'function', 'function': {'name': 'numeros', 'description': 'Quanto o grupo está preenchido, quantos valores diferentes e quantas vezes aparece por registro.', 'parameters': {'type': 'object', 'properties': {'grupo': {'type': 'string'}}, 'required': ['grupo']}}},
]

def ferramenta(r, nome, grupo):
    g = next((x for x in r['grupos'] if x['nome'] == grupo), None)
    if not g: return 'grupo não encontrado; grupos de data existentes: ' + ', '.join(x['nome'] for x in r['grupos'] if x.get('tipo_maioria') == 'data')
    if nome == 'exemplos': return ', '.join(list(dict.fromkeys(c[3] for c in g['cel']))[:10])
    if nome == 'vizinhos':
        v = [x.rstrip(':') for x, _ in (g.get('viz_todos') or {}).items() if x.rstrip(':') != grupo]
        return ('rótulos por perto: ' + ', '.join(v)) if v else 'nenhum rótulo por perto (o relatório não tem cabeçalho nessa parte)'
    if nome == 'ordem_no_tempo':
        ls = ['"%s" vem antes de "%s" (diferença típica %s)' % (n['antes'], n['depois'], n['tipico']) for n in r['datas'] if grupo in (n['antes'], n['depois'])]
        outras = [x['nome'] for x in r['grupos'] if x.get('tipo_maioria') == 'data' and x['nome'] != grupo]
        return ('; '.join(ls) if ls else 'sem comparação de tempo disponível') + ' | outros grupos de data: ' + (', '.join(outras) or 'nenhum')
    if nome in ('arredores', 'trecho'):
        L = r['_linhas']; cels = [c for c in g['cel'] if c[1]][:: max(1, len(g['cel']) // 3)][:3]
        if not cels: return 'sem posição no arquivo (valor de contexto)'
        if nome == 'trecho':
            li = cels[0][1]; return '\n'.join(' | '.join(x for x in L[i] if x) for i in range(max(0, li - 3), min(len(L), li + 2)))
        out = []
        for _, li, co, v in cels:
            lin = L[li - 1]; ant = [x for x in lin[:co - 1] if x][-2:]; dep = [x for x in lin[co:] if x][:2]
            cima = ' | '.join(x for x in L[li - 2] if x) if li >= 2 else ''; baixo = ' | '.join(x for x in L[li] if x) if li < len(L) else ''
            out.append('em cima: [%s] / antes: [%s] VALOR: %s depois: [%s] / embaixo: [%s]' % (cima[:120], ' | '.join(ant), v, ' | '.join(dep), baixo[:120]))
        return '\n'.join(out)
    if nome == 'numeros':
        return 'preenchido em %d%% dos registros; %d valores diferentes; até %d por registro' % (g['preenchido'] * 100, len(set(c[3] for c in g['cel'])), g['lista'])
    return 'ferramenta desconhecida'


def pistas_de(r, grupo):
    g = next(x for x in r['grupos'] if x['nome'] == grupo)
    sem_nome = '(sem nome)' in grupo
    out = ['Relatório: %s (%d registros).' % (r['arquivo'], r['registros']),
           'Grupo: "%s"%s.' % (grupo, ' (este grupo NÃO tem rótulo no relatório)' if sem_nome else ' (este é o rótulo escrito no relatório)')]
    for nome, tit in [('exemplos', 'Exemplos'), ('vizinhos', 'Vizinhos'), ('ordem_no_tempo', 'Ordem no tempo'), ('numeros', 'Números'), ('arredores', 'Arredores no arquivo')]:
        out.append(tit + ': ' + ferramenta(r, nome, grupo))
    return '\n'.join(out)
