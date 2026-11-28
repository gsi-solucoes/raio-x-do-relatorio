"""Gera a página de teste do Gemini Nano (IA embutida no Chrome) com as perguntas de data dos arquivos FICTÍCIOS (lote1).
O script junta todas as pistas (o que as ferramentas do ia_teste.py dariam) e a IA só decide. Uso:
python3 -I teste_gemini.py saida.html"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import formula as F
from ia_teste_pistas import pistas_de
AQUI = os.path.dirname(os.path.abspath(__file__))
LOTE = os.path.join(AQUI, '..', 'dados-ficticios', 'lote1')
gab = json.load(open(os.path.join(AQUI, 'gabarito_datas.json'), encoding='utf-8'))
casos = []
for arq, esp in gab.items():
    cam = os.path.join(LOTE, arq)
    if not os.path.exists(cam): continue                      # só fictícios; reais ficam fora
    L = F.ler(cam)[0]; r = F.montar(L, cam); r['_linhas'] = L
    for grupo, certo in esp.items():
        regra = next((x['qual_data']['sig'] for x in r['grupos'] if x['nome'] == grupo and 'qual_data' in x), '?')
        antes = [n['antes'] for n in r['datas'] if n['depois'] == grupo]; depois = [n['depois'] for n in r['datas'] if n['antes'] == grupo]
        casos.append({'arquivo': arq, 'grupo': grupo, 'certo': certo, 'regras': regra, 'dossie': pistas_de(r, grupo), 'antes': antes, 'depois': depois})
modelo = open(os.path.join(AQUI, 'teste_gemini_modelo.html'), encoding='utf-8').read()
open(sys.argv[1], 'w', encoding='utf-8').write(modelo.replace('/*CASOS*/[]', json.dumps(casos, ensure_ascii=False)))
print(len(casos), 'perguntas; regras acertam', sum(c['regras'] == c['certo'] for c in casos))
