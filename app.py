from flask import Flask, render_template, request, redirect, url_for

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
        manutencao = request.form.get('manutencao')
        hinicial_manutencao = request.form.get('manutencao_horimetro_inicial')
        hfinal_manutencao = request.form.get('manutencao_horimetro_final')
        tempo_manutencao = request.form.get('tempo_manutencao')
        transporte_pracha = request.form.get('transporte_pracha')

        # Formatação do relatório em string
        relatorio = f"""
        DATA: {data}
        FAZENDA: {fazenda}
        TALHAO: {talhao}
        TURNO: {turno}
        STATUS: {status}
        Máquina: {maquina}
        Operador: {operador}
        Horímetro Inicial: {hinicial}
        Horímetro Final: {hfinal}
        Horas Trabalhadas: {horas_trabalhadas}
        Produção Ha: {producao_ha}
        Equipe em Transporte: {equipe_transporte}
        DDS/Café: {dds_cafe}
        Inspensão Diária: {manutencao} - Início: {hinicial_manutencao}, Final: {hfinal_manutencao}
        Tempo de Manutenção: {tempo_manutencao}
        Em Transporte de Prancha: {transporte_pracha}
        """

        # Enviar relatório para o template `report.html`
        return render_template('report.html', relatorio=relatorio)

if __name__ == '__main__':
    app.run(debug=True)
