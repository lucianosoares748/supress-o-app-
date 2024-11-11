function calcularHoras() {
  const hinicial = parseFloat(document.getElementById("hinicial").value);
  const hfinal = parseFloat(document.getElementById("hfinal").value);

  if (!isNaN(hinicial) && !isNaN(hfinal) && hfinal >= hinicial) {
    let horasTrabalhadas = hfinal - hinicial;
    // Aplica toFixed(1) e converte para ponto decimal fixo
    document.getElementById("horas_trabalhadas").value = horasTrabalhadas.toFixed(1).replace(',', '.');
  } else {
    alert("Verifique os valores dos horímetros.");
  }
}






function calcularTempoManutencao(button) {
  const bloco = button.closest(".bloco-manutencao");
  const inicio = bloco.querySelector(".horario-inicial").value;
  const fim = bloco.querySelector(".horario-final").value;

  if (inicio && fim) {
    const [inicioHoras, inicioMinutos] = inicio.split(":").map(Number);
    const [fimHoras, fimMinutos] = fim.split(":").map(Number);

    const minutosInicio = inicioHoras * 60 + inicioMinutos;
    const minutosFim = fimHoras * 60 + fimMinutos;

    const diferencaMinutos = minutosFim - minutosInicio;
    const horas = Math.floor(diferencaMinutos / 60);
    const minutos = diferencaMinutos % 60;

    bloco.querySelector(".tempo-manutencao").value = `${horas}h ${minutos}min`;
  } else {
    alert("Por favor, insira os horários de início e fim da manutenção.");
  }
}




let manutencaoIndex = -0;

function adicionarBlocoManutencao() {
    const blocoManutencao = document.createElement('div');
    blocoManutencao.classList.add('bloco-manutencao');
    
    blocoManutencao.innerHTML = `
        <div class="form-group">
          <label for="manutencao_${manutencaoIndex}">Tipo de Manutenção:</label>
          <select name="manutencao_${manutencaoIndex}" class="manutencao" required>
            <option selected disabled value>Selecione</option>
            <option value="Afiação de Facas">Afiação de Facas</option>
            <option value="Substituição de facas">Substituição de facas</option>
            <option value="Perca de potência">Perca de potência</option>
            <option value="Substituição de rolamento frontal">Substituição de rolamento frontal</option>
            <option value="Substituição de rolamento traseiro">Substituição de rolamento traseiro</option>
            <option value="Substituição de polia">Substituição de polia</option>
            <option value="Substituição de correia do cabeçote">Substituição de correia do cabeçote</option>
            <option value="Retirada de arame do rolo">Retirada de arame do rolo</option>
            <option value="Trava aranha">Trava aranha</option>
            <option value="Manutencao preventiva">Manutencao preventiva</option>
            <option value="Troca de correia do cabecote">Troca de correia do cabecote</option>
          </select>
        </div>
        <div class="form-group">
          <label>Horário Inicial (Manutenção):</label>
          <input type="time" name="manutencao_horimetro_inicial_${manutencaoIndex}" class="horario-inicial">
        </div>
        <div class="form-group">
          <label>Horário Final (Manutenção):</label>
          <input type="time" name="manutencao_horimetro_final_${manutencaoIndex}" class="horario-final">
        </div>
        <div class="form-group">
          <button type="button" onclick="calcularTempoManutencao(this)">Calcular Tempo em Manutenção</button>
          <input type="text" name="tempo_manutencao_${manutencaoIndex}" class="tempo-manutencao" readonly>
        </div>
    `;

    document.getElementById('blocos-manutencao').appendChild(blocoManutencao);
    manutencaoIndex++;
}
