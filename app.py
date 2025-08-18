from flask import Flask, render_template, request
from datetime import datetime

# Cria a aplicação Flask
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Formata a data para DD/MM/YYYY
        data_raw = request.form.get('data')
        data_formatada = datetime.strptime(data_raw, "%Y-%m-%d").strftime("%d/%m/%Y")

        fazenda = request.form.get('fazenda')
        talhao = request.form.get('talhao')
        turno = request.form.get('turno')
        status = request.form.get('status')
        maquina = request.form.get('maquina')
        operador = request.form.get('operador')
        hinicial = request.form.get('horimetro_inicial')
        hfinal = request.form.get('horimetro_final')
        horas_trabalhadas = request.form.get('horas_trabalhadas')
        producao_ha = request.form.get('producao_ha')
        equipe_transporte = request.form.get('equipe_transporte')
        dds_cafe = request.form.get('dds_cafe')
        transporte_pracha = request.form.get('transporte_pracha')

        # Captura múltiplas entradas de manutenção
        manutencoes = []
        index = 0
        while f'manutencao_{index}' in request.form:
            manutencao = request.form.get(f'manutencao_{index}')
            if manutencao:  # só adiciona se tiver valor
                manutencoes.append({
                    "tipo": manutencao,
                    "horario_inicial": request.form.get(f'manutencao_horimetro_inicial_{index}'),
                    "horario_final": request.form.get(f'manutencao_horimetro_final_{index}'),
                    "tempo": request.form.get(f'tempo_manutencao_{index}')
                })
            index += 1

        # Monta o relatório com espaçamento correto
        relatorio = (
            f"DATA: {data_formatada}\n"
            f"FAZENDA: {fazenda}\n"
            f"TALHÃO: {talhao}\n"
            f"TURNO: {turno}\n"
            f"STATUS: {status}\n"
            f"MÁQUINA: {maquina}\n"
            f"OPERADOR: {operador}\n"
            f"HORÍMETRO INICIAL: {hinicial}\n"
            f"HORÍMETRO FINAL: {hfinal}\n"
            f"HORAS TRABALHADAS: {horas_trabalhadas}\n"
            f"PRODUÇÃO HA: {producao_ha}\n"
            f"EQUIPE EM TRANSPORTE: {equipe_transporte}\n"
            f"DDS/CAFÉ: {dds_cafe}\n"
        )

        relatorio += "\nINSPEÇÃO DIÁRIA:\n"
        for i, m in enumerate(manutencoes):
            relatorio += (
                f"\nMANUTENÇÃO {i+1}:\n"
                f"- Tipo: {m['tipo']}\n"
                f"- Horário Inicial: {m['horario_inicial']}\n"
                f"- Horário Final: {m['horario_final']}\n"
                f"- Tempo: {m['tempo']}\n"
            )

        relatorio += f"\nEM TRANSPORTE DE PRANCHA: {transporte_pracha}\n"

        return render_template('report.html', relatorio=relatorio)

if __name__ == '__main__':
    app.run(debug=True)
