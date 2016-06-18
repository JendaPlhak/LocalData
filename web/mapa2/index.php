<? require '../header.php' ?>

<div class="row">
  <div class="col-md-2">
    <div class="checkbox">
     <label for="pronajem">
       <input type="checkbox"> Pronájem
     </label>
    </div>
    <div class="checkbox">
     <label for="prodej">
       <input type="checkbox"> Prodej
     </label>
    </div>
    <div class="checkbox">
     <label for="byt">
       <input type="checkbox"> Byt
     </label>
    </div>
    <div class="checkbox">
     <label for="nebytove_prostory">
       <input type="checkbox"> Nebytové prostory
     </label>
    </div>
  </div>
  <div class="col-md-10">

<div id="map"></div>

<link rel="stylesheet" href="https://cartodb-libs.global.ssl.fastly.net/cartodb.js/v3/3.15/themes/css/cartodb.css" />
<script src="https://cartodb-libs.global.ssl.fastly.net/cartodb.js/v3/3.15/cartodb.js"></script>

<script>
  var map = new L.Map('map', {
    center: [0,0],
    zoom: 2
  })
  cartodb.createLayer(map, 'https://examples.cartodb.com/api/v1/viz/15589/viz.json', { https: true })
    .addTo(map)
    .on('error', function(err) {
      alert("some error occurred: " + err);
    });
</script>



    <div width="100%" height="520" frameborder="0" 
      id="map"
      xxxsrc="https://localinfo.cartodb.com/viz/c6eb0296-3547-11e6-b73f-0e787de82d45/embed_map" allowfullscreen webkitallowfullscreen mozallowfullscreen oallowfullscreen msallowfullscreen>
    </div>

  </div>
</div>

<xscript>
  cartodb.createVis('map', 'https://localinfo.cartodb.com/api/v2/viz/c6eb0296-3547-11e6-b73f-0e787de82d45/viz.json');
</xscript>

<? require '../footer.php' ?>