from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Renderiza o formulário

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Pega os dados do formulário
        data = request.form.get('data')
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
                index += 1  # Incrementa o índice para capturar a próxima manutenção
            else:
                break  # Interrompe o loop quando não há mais entradas de manutenção

        # Formatação do relatório em string
        relatorio = f"""
        *DATA:* {data}
        *FAZENDA:* {fazenda}
        *TALHÃO:* {talhao}
        *TURNO:* {turno}
        *STATUS:* {status}
        *MÁQUINA:* {maquina}
        *OPERADOR:* {operador}
        *HORÍMETRO INICIAL:* {hinicial}
        *HORÍMETRO FINAL:* {hfinal}
        *HORAS TRABALHADAS:* {horas_trabalhadas}
        *PRODUÇÃO HA:* {producao_ha}
        *EQUIPE EM TRANSPORTE:* {equipe_transporte}
        *DDS/CAFÉ:* {dds_cafe}
        """

        # Adiciona o bloco de inspeção diária ao relatório
        relatorio += "\nINSPEÇÃO DIÁRIA:\n"
        for i, m in enumerate(manutencoes):
            relatorio += f"""
            MANUTENÇÃO {i+1}:
            - Tipo: {m['tipo']}
            - Horário Inicial: {m['horario_inicial']}
            - Horário Final: {m['horario_final']}
            - Tempo: {m['tempo']}
            """

        # Finaliza o relatório com o transporte de prancha
        relatorio += f"\nEM TRANSPORTE DE PRANCHA: {transporte_pracha}\n"

        # Envia o relatório para o template `report.html`
        return render_template('report.html', relatorio=relatorio)

if __name__ == '__main__':
    app.run(debug=True)
