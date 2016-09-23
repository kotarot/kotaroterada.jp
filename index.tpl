<!DOCTYPE html>
<html lang="{{ page.lang }}">
 <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# article: http://ogp.me/ns/article#">
  <meta charset="UTF-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=Edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{{ page.title }}</title>
  <link rel="stylesheet" href="skyline/css/screen.css" />
  <link rel="stylesheet" href="style.css" />
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
    background-image: url("./zedboard.jpg");
    background-position: center center;
    color: #fff;
    height: 250px;
}
</style>
 </body>
</html>
