const container = document.getElementsByClassName("informacoes-do-calculo")[0];
const input_eq = document.getElementById("entrada-equacao");

const eq_armazenada = sessionStorage.getItem('equacao');

// Condição para que a equação seja armazenada
function condicaoArmazenamento() {
    return (!(input_eq.value === eq_armazenada) && (input_eq.value.trim() != ''));
}

// Condição para que as informacões sejam geradas
function condicaoRenderizacao() {
    return (condicaoArmazenamento() && (!document.getElementById('ver-grafico')));
}

// Função de armazenar a equacao
function armazenarEquacao(){
    if ( condicaoArmazenamento() ){
        sessionStorage.setItem('equacao', input_eq.value)
        }
}
// Função de gerar o botão ver-grafico
function verGrafico(){

    if ( condicaoRenderizacao() ) {
        
        // Informações do botão a ser gerado
        const plotar = document.createElement('button');
        plotar.innerText = "VER GRÁFICO";
        plotar.id = "ver-grafico";
        // Plotar gáfico ao clicar no botão gerado
        plotar.addEventListener('click', () => {plotar_gf(), initGeoGebra()});
            
        // Gerar botão
        container.appendChild(plotar);
    }
}

// Função para plotar o gráfico da função armazenada
function plotar_gf(){
    // Gera a interface do Geogebra num IFrame
    if (!document.getElementById("interface-da-plotagem")) {
        
        // Cria a div que hospedará o Geogebra
        const interface_da_plotagem = document.createElement('div');
        interface_da_plotagem.id = "interface-da-plotagem";
        container.appendChild(interface_da_plotagem);
    }
}


// Informações geradas ao escolher a opcão "Falsa Posição"
const gerarInformacoesFalsaPosicao = (  ) => {
    armazenarEquacao();
    verGrafico();
}

// Informações geradas ao escolher a opcão "Newthon-Raphson"
const gerarInformacoesNewthonRaphson = (  ) => {
    armazenarEquacao();
    verGrafico();
}