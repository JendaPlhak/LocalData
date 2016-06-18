<? require('header.php') ?>

  <div id="sidebar">
    <p>Lokálka vám řekne kolik stojí domy a byty ve vašem okolí</p>
    <p>Projekt vyznikl v rámci WhatTheHack</p>
  </div>
  <div id="map"></div>

    <script>

    var map = new L.Map('map', { 
      center: [50.09087,14.40265],
      zoom: 19
    });

    L.tileLayer('http://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png',{
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
    }).addTo(map);

//    var layerUrl = 'https://localinfo.cartodb.com/api/v2/viz/c6eb0296-3547-11e6-b73f-0e787de82d45/viz.json'; // puvodni heatmap
    var layerUrl = 'https://localinfo.cartodb.com/api/v2/viz/3212d9c4-35a5-11e6-ae36-0ea31932ec1d/viz.json';

//    var layerUrl = 'http://documentation.cartodb.com/api/v2/viz/2b13c956-e7c1-11e2-806b-5404a6a683d5/viz.json';


  cartodb.createVis('map', layerUrl)
  .done(function(vis, layers) {
    // layer 0 is the base layer, layer 1 is cartodb layer
    // when setInteraction is disabled featureOver is triggered
//    window.test = layers[0];
//    layers[1].createSubLayer({
//      sql: "SELECT * FROM table_name limit 200",
//      cartocss: '#table_name {marker-fill: #F0F0F0;}'
//    });



//    layers[0].on('featureOver', function(e, latlng, pos, data, layerNumber) {
//      console.log(e, latlng, pos, data, layerNumber);
//    });

    // you can get the native map to work with it
    var map = vis.getNativeMap();

    // now, perform any operations you need, e.g. assuming map is a L.Map object:
    map.setZoom(19);
    map.panTo([50.09087,14.40265]);
  });

//    cartodb.createLayer(map, layerUrl)
//      .addTo(map)
//      .on('done', function(layer) {
//        layer.setInteraction(true);
//        layer.on('featureOver', function(e, latlng, pos, data, layerNumber) {
//           console.log(e, latlng, pos, data, layerNumber);
//        });
//      });

    </script>

<? require('footer.php') ?>
