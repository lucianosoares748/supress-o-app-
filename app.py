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
            f"Data: {data_formatada}\n"
            f"Fazenda: {fazenda}\n"
            f"Talhão: {talhao}\n"
            f"Turno: {turno}\n"
            f"Status: {status}\n"
            f"Máquina: {maquina}\n"
            f"Operador: {operador}\n"
            f"Horímetro Inicial: {hinicial}\n"
            f"Horímetro Final: {hfinal}\n"
            f"Horas Trabalhadas: {horas_trabalhadas}\n"
            f"Produção HA: {producao_ha}\n"
            f"Equipe em Transporte: {equipe_transporte}\n"
            f"DDS/CAFÉ: {dds_cafe}\n"
        )

        relatorio += "\nInspensão diária:\n"
        for i, m in enumerate(manutencoes):
            relatorio += (
                f"\nManutenção {i+1}:\n"
                f"- Tipo: {m['tipo']}\n"
                f"- Horário Inicial: {m['horario_inicial']}\n"
                f"- Horário Final: {m['horario_final']}\n"
                f"- Tempo: {m['tempo']}\n"
            )

        relatorio += f"\nEm Transporte Prancha: {transporte_pracha}\n"

        return render_template('report.html', relatorio=relatorio)

if __name__ == '__main__':
    app.run(debug=True)
