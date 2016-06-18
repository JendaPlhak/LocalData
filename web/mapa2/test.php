<? require('../header.php') ?>

    <div id="map"></div>

    <!-- include cartodb.js library -->
    <script src="http://libs.cartocdn.com/cartodb.js/v3/3.15/cartodb.js"></script>

    <script>
      function main() {
        cartodb.createVis('map', 'http://documentation.cartodb.com/api/v2/viz/2b13c956-e7c1-11e2-806b-5404a6a683d5/viz.json', {
            shareable: true,
            title: true,
            description: true,
            search: true,
            tiles_loader: true,
            center_lat: 0,
            center_lon: 0,
            zoom: 2
        })
      }

      window.onload = main;
    </script>
  </body>
</html>