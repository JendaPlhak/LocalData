<!DOCTYPE html>
<html lang="en">
  <head profile="http://www.w3.org/2005/10/profile">
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="./favicon.ico">

    <title>Lokálka :: vám řekne kolik stojí byty v okolí</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="http://libs.cartocdn.com/cartodb.js/v3/3.15/themes/css/cartodb.css" />
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
    <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">

    <link rel="icon" type="image/png" href="./favicon.png">

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
    <script src="http://libs.cartocdn.com/cartodb.js/v3/3.15/cartodb.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/js/bootstrap.min.js"></script>

  <style>
    html, body, #container {
      height: 100%;
      width: 100%;
      overflow: hidden;
    }

    body {
      padding-top: 50px;
    }

    #map {
      padding-left:250px;
      width: 100%;
      height: 100%;
      box-shadow: 0 0 10px rgba(0,0,0,0.55);
    }

    #sidebar {
      position: realtive;
      width: 250px;
      padding:20px;
      height: 100%;
      max-width: 100%;
      float: left;
      -webkit-transition: all 0.25s ease-out;
      -moz-transition: all 0.25s ease-out;
      transition: all 0.25s ease-out;
    }

    .navbar .navbar-brand {
      font-weight: bold;
      font-size: 25px;
      color: #FFFFFF;
    }

    .navbar {
      background-image: linear-gradient(to bottom, #2b6988 0%, #1f4b61 100%);
    }

    .navbar-inverse .navbar-nav>li>a {
      color: #fff;
    }
  </style>

  </head>
  <body>

    <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
      <div class="container-fluid">
        <div class="navbar-header">
          <div class="navbar-icon-container">
            <a href="#" class="navbar-icon pull-right visible-xs" id="nav-btn"><i class="fa fa-bars fa-lg white"></i></a>
            <a href="#" class="navbar-icon pull-right visible-xs" id="sidebar-toggle-btn"><i class="fa fa-search fa-lg white"></i></a>
          </div>
          <a class="navbar-brand" href="#">Lokálka</a>
        </div>
        <div class="navbar-collapse collapse">
          <form class="navbar-form navbar-right" role="search">
            <div class="form-group has-feedback">
                <span class="twitter-typeahead" style="position: static; display: block; direction: ltr;">
                  <input id="searchbox" type="text" placeholder="Hledej" class="form-control tt-input" autocomplete="off" spellcheck="false" dir="auto" style="position: relative; vertical-align: top;">
                     <pre aria-hidden="true" style="position: absolute; visibility: hidden; white-space: pre; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 14px; font-style: normal; font-variant: normal; font-weight: 400; word-spacing: 0px; letter-spacing: 0px; text-indent: 0px; text-rendering: auto; text-transform: none;"></pre>
                     <span class="tt-dropdown-menu" style="position: absolute; top: 100%; left: 0px; z-index: 100; display: none; right: auto;">
                  <div class="tt-dataset-Boroughs"></div><div class="tt-dataset-Theaters"></div>
                  <div class="tt-dataset-Museums"></div><div class="tt-dataset-GeoNames"></div></span>
                </span>
                <span id="searchicon" class="fa fa-search form-control-feedback"></span>
            </div>
          </form>
          <ul class="nav navbar-nav">
            <li><a href="#" id="btnAbout"><i class="fa fa-question-circle white"></i>&nbsp;&nbsp;O projektu</a></li>
            <li class="hidden-xs"><a href="#" id="btnLegenda"><i class="fa fa-list white"></i>&nbsp;&nbsp;Filtrování</a></li>
          </ul>
        </div><!--/.navbar-collapse -->
      </div>
    </div>

    <div id="container">
