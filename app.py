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
        while True:
            manutencao = request.form.get(f'manutencao_{index}')
            if manutencao:
                hinicial_manutencao = request.form.get(f'manutencao_horimetro_inicial_{index}')
                hfinal_manutencao = request.form.get(f'manutencao_horimetro_final_{index}')
                tempo_manutencao = request.form.get(f'tempo_manutencao_{index}')
                manutencoes.append({
                    "tipo": manutencao,
                    "horario_inicial": hinicial_manutencao,
                    "horario_final": hfinal_manutencao,
                    "tempo": tempo_manutencao
                })
                index += 1
            else:
                break

        # Monta o relatório
        relatorio = f"""
        DATA: {data_formatada}
        FAZENDA: {fazenda}
        TALHÃO: {talhao}
        TURNO: {turno}
        STATUS: {status}
        MÁQUINA: {maquina}
        OPERADOR: {operador}
        HORÍMETRO INICIAL: {hinicial}
        HORÍMETRO FINAL: {hfinal}
        HORAS TRABALHADAS: {horas_trabalhadas}
        PRODUÇÃO HA: {producao_ha}
        EQUIPE EM TRANSPORTE: {equipe_transporte}
        DDS/CAFÉ: {dds_cafe}
        """

        relatorio += "\nINSPEÇÃO DIÁRIA:\n"
        for i, m in enumerate(manutencoes):
            relatorio += f"""
            MANUTENÇÃO {i+1}:
            - Tipo: {m['tipo']}
            - Horário Inicial: {m['horario_inicial']}
            - Horário Final: {m['horario_final']}
            - Tempo: {m['tempo']}
            """

        relatorio += f"\nEM TRANSPORTE DE PRANCHA: {transporte_pracha}\n"

        return render_template('report.html', relatorio=relatorio)

if __name__ == '__main__':
    app.run(debug=True)
