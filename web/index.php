<? require('header.php') ?>

  <div id="sidebar">
   <div id="sidebar1">
    <p>Lokálka vám řekne kolik stojí byty ve lokalitě která vás zajímá</p>

    <p>
      <h4>Výtah</h4>
      <div class="btn-group" role="group" aria-label="Výtah">
        <button type="button" class="btn btn-lg btn-default btn-success" id="btnVytahVyp">je mi jedno</button>
        <button type="button" class="btn btn-lg btn-default" id="btnVytahZap">chci</button>
      </div>
    </p>
<!--    <br/>
    <input type="checkbox" aria-label="vytah" id="chbVytah"> chci výtah
    <br/>
    <p><a class="btn btn-lg btn-success" href="#" role="button" id="btnVytah">S výtahem i bez</a></p>
    <p><a class="btn btn-lg btn-success" href="#" role="button" id="btnPlyn">S plynem i bez</a></p>
-->
    <p>
      <h4>Plyn</h4>
      <div class="btn-group" role="group" aria-label="Plyn">
        <button type="button" class="btn btn-lg btn-default btn-success" id="btnPlynVyp">je mi jedno</button>
        <button type="button" class="btn btn-lg btn-default" id="btnPlynZap">chci</button>
      </div>
    </p>

    <p>
      <label for="amount">Cena za byt</label>
      <input type="text" id="amount" readonly style="border:0; color:rgb(92, 184, 92); font-weight:bold;">
      <div id="slider-range"></div>
    </p>
   </div>
   <div id="sidebar2" class="hidden" style="font-size:80%">
    <p>Lokálka umožňuje přehledně procházet ceny a další údaje o bytech ve vaší lokalitě.
       Pomocí hledání, nebo zazoomovánám mapy (kromě  +/- funguje i Shift+drag myší) najděte lokalitu,
       která vás zajímá. Byty jsou barveny podle ceny a lze je filtrovat. Informace o konkrétním bytě můžete získat najetím na
       něj, kliknutím se zobrazí další info.
    </p>
    <p>Lokálka vyznikla za pouhých 28 hodin v rámci <a href="http://whatthehack.cz/">WhatTheHack</a> hackatlonu, jako
      ukázka toho co lze dosáhnout s dobrým teamem, za velmi krátký čas. Pokud máte chuť v práci pokračovat, forkněte si projekt na 
      <a href="https://github.com/JendaPlhak/LocalData">githubu</a> je k dispozici pod 
      <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">CC BY</a> licencí.
    </p>
    <p>
      Na projektu se podíleli: <b>(prosím napište mi na slack jak chcete být uvedeni a případný  link)</b> <a href="https://github.com/gorn">gorn</a>, Jenda Plhák, Zbyněk Růžička, Zdeněk Softič
Bert Šváb, Barbora Ulipová, Jan Cibulka a především náš mentor Marek Aufart. Veliký dík patří organizátorům hackatlonu, WhatTheHack, skvěle jsme si to užili.
    </p>
    <p style="text-align:right"><i>Lokálka team</i></p>
   </div>
  </div>
  <div id="map"></div>

    <script>
      var layerUrl = 'https://localinfo.cartodb.com/api/v2/viz/641d3b26-3609-11e6-b753-0ea31932ec1d/viz.json';
  cartodb.createVis('map', layerUrl)
  .done(function(vis, layers) {
    var map = vis.getNativeMap();

    // now, perform any operations you need, e.g. assuming map is a L.Map object:
    map.setZoom(14);
    map.panTo([50.0713,14.4236]);

    $(document).ready(function(){
      dataLayer = vis.getLayers()[1].getSubLayer(0);

      function refreshSQL() {
        var sql = "SELECT * FROM wth_table_ws_filled_2 WHERE ";
        var min =  $( "#slider-range" ).slider( "values", 0 )/5 * 1000000
        var max =  $( "#slider-range" ).slider( "values", 1 )/5 * 1000000
        sql = sql + min + " < cena AND cena < " + max

        if ($('#btnVytahZap').hasClass('btn-success')) {
          sql = sql +  " AND vytah='s vytahem'";
        };
        if ($('#btnPlynZap').hasClass('btn-success')) {
          sql = sql +  " AND (plyn='plyn z domovniho zasobniku' OR plyn='plyn z verejne site')";
        };
        dataLayer.setSQL(sql);
      };

      $( "#slider-range" ).slider({
        range: true,
        min: 0,
        max: 75,
        values: [ 0, 75 ],
        slide: function( event, ui ) {
          $( "#amount" ).val( ui.values[ 0 ]/5 + " - " + ui.values[ 1 ]/5 + " mil Kč" );
        },
        stop: function( event, ui ) {refreshSQL();}
      });
      $( "#amount" ).val( $( "#slider-range" ).slider( "values", 0 )/5 +
        " - " + $( "#slider-range" ).slider( "values", 1 )/5 + " mil Kč" );

      $('#btnVytahVyp').on('click', function(){
        if(!$(this).hasClass('btn-success')) { 
          $(this).toggleClass('btn-success');
          $('#btnVytahZap').toggleClass('btn-success');
        };
        refreshSQL();
      });

      $('#btnVytahZap').on('click', function(){
        if(!$(this).hasClass('btn-success')) { 
          $(this).toggleClass('btn-success');
          $('#btnVytahVyp').toggleClass('btn-success');
        };
        refreshSQL();
      });

      $('#btnPlynVyp').on('click', function(){
        if(!$(this).hasClass('btn-success')) { 
          $(this).toggleClass('btn-success');
          $('#btnPlynZap').toggleClass('btn-success');
        };
        refreshSQL();
      });

      $('#btnPlynZap').on('click', function(){
        if(!$(this).hasClass('btn-success')) { 
          $(this).toggleClass('btn-success');
          $('#btnPlynVyp').toggleClass('btn-success');
        };
        refreshSQL();
      });

      $('#btnPlyn').on('click', function(){
        if($(this).hasClass('zapnuto')) { 
          $(this).html('S plynem i bez');
        } else {
          $(this).html('Jen s plynem');
        };
        $(this).toggleClass('zapnuto');
        refreshSQL();
      });

      $('#btnAbout').on('click', function(){
        $('#sidebar1').addClass('hidden');
        $('#sidebar2').removeClass('hidden');
      });

      $('#btnLegenda').on('click', function(){
        $('#sidebar2').addClass('hidden');
        $('#sidebar1').removeClass('hidden');
      });

    });
  });



    </script>

<? require('footer.php') ?>
