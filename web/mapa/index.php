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
    <iframe width="100%" height="520" frameborder="0" src="https://localinfo.cartodb.com/viz/c6eb0296-3547-11e6-b73f-0e787de82d45/embed_map" allowfullscreen webkitallowfullscreen mozallowfullscreen oallowfullscreen msallowfullscreen></iframe>
    </iframe>
  </div>
</div>

<? require '../footer.php' ?>