<!DOCTYPE html>
<html lang="{{ page.lang }}">
 <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# article: http://ogp.me/ns/article#">
  <meta charset="UTF-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=Edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{{ page.title }}</title>
  <link rel="stylesheet" href="static/skyline/css/screen.css" />
  <link rel="stylesheet" href="static/style/style.css" />
  <link rel="stylesheet" href="https://afeld.github.io/emoji-css/emoji.css" />
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.1.0/css/all.css" integrity="sha384-lKuwvrZot6UHsBSfcMvOkWwlCMgc0TaWr+30HWe3a4ltaBwTZhyTEggF5tJv8tbt" crossorigin="anonymous" />
  <link rel="canonical" href="{{ page.canonical }}" />
  <!--[if lt IE 9]>
  <script src="//oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
  <script src="//oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
  <![endif]-->
  <meta name="description" content="{{ page.description }}" />
  <meta name="keywords" content="{{ page.keywords }}" />
  <meta property="og:locale" content="{{ ogp.locale }}" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{{ ogp.title }}" />
  <meta property="og:url" content="{{ ogp.url }}" />
  <meta property="og:description" content="{{ page.description }}" />
  <meta property="og:site_name" content="{{ ogp.sitename }}" />
  <meta property="og:image" content="{{ ogp.image }}" />
 </head>
 <body>
  <div class="site">
    {{ content }}
  </div>
<style>
.site-header {
    background-image: url("./{{ page.bgphoto }}");
    background-position: center center;
    color: #fff;
    height: 250px;
}
</style>

<script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
<script>
$(function() {
    var container_width = $('section#container-0').width();
    var original_width = $('iframe.youtube').attr('width');
    var original_height = $('iframe.youtube').attr('height');
    if (container_width < 580) {
        var height = (container_width) * original_height / original_width;
        $('iframe.youtube').attr('width', container_width);
        $('iframe.youtube').attr('height', height);
    }
});
</script>

 </body>
</html>
