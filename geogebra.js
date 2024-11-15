var ggbApplet;

function initGeoGebra() {
/*     console.log('geogebra iniciado')
    // Criação do applet do GeoGebra
    ggbApplet = new GGBApplet({
        "id": "geogebra",
        "appName": 'graphing',
        "width": 600,
        "height": 600,
        "showToolBar": false,
        "borderColor": null,
        "showMenuBar": false,
        "allowStyleBar": false,
        "showAlgebraInput": true,
    }, true);
    
    // Injeção do applet no elemento HTML
    ggbApplet.inject('interface-da-plotagem');

    window.onload = initGeoGebra; */

    window.open('./grafico.html')
}