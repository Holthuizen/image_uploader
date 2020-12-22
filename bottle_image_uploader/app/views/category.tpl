<head>
<link rel="preconnect" href="https://fonts.gstatic.com">
<link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
<title>Image Uploader By Carlos</title>
</head>

<style>
body { 
  font-size: 2rem; 
  font-family: 'Roboto', sans-serif;
  background-color: #d4d4d4; 
  padding-left:  1rem; 
  padding-right: 2rem;
 }

 
input[type=text] {
  padding: 15px 32px;
  width: 350px; /* When specifying this, you can use both px and % */
  font-size: 16px;
  border: none;
}

input[type=button] {
  background-color: #4CAF50; /* Green */
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
}

 
img {max-width:900px; height: auto}
button #delete {background-color: red}
</style>

<body>
    <input type="button" id="Home" onclick="location.href='{{server}}';" value="#home" /> 
    <hr>
    <br>

    % for item in collection:
      <a id="short_url" href="{{item['copy_url']}}"> <img src="{{item['full_url']}}"> </a>
      <br>
      <input type="text" value="{{item['copy_url']}}" id="{{item['copy_url']}}"> <input type="button" onclick="copy_short_url( '{{item['copy_url']}}' )" value="#Copy (short) URL" /> 
      <input type="button" onclick="location.href='{{item['download_url']}}';" value="#Download" /> 
      <br>
      <br>
    % end
</body>


<script>
function copy_short_url(short_url) {
  /* Get the text field */
  var copyText = document.getElementById(short_url);

  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */

  /* Copy the text inside the text field */
  document.execCommand("copy");

  /* Alert the copied text */
  alert("Copied the text: " + copyText.value);
} 
</script>