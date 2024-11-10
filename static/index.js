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
