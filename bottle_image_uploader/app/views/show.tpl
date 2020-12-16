<style>
body {background-color: #d4d4d4; padding: 2rem}
img {max-width:auto; height: auto}

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

#delete {background-color: #f44336; borther}

</style>

<br>
<h3>Category:  
<a href="{{ category_url }}">{{category}}</a> </h3>
<input type="button" id="Home" onclick="location.href='{{server}}';" value="#home" />
<hr> <br> 
<body>
    <a id="short_url" href="{{short_url}}"><img src="{{url}}"></a><br>
    <br>
    <input type="text" value="{{short_url}}" id="short_url">
    <input type="button" onclick="location.href='{{download_url}}';" value="#Download" />
    <input type="button" id="delete" onclick="location.href='{{delete_url}}';" value="#Delete" />
</body>


<script>
function copy_short_url() {
  /* Get the text field */
  var copyText = document.getElementById("short_url");

  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */

  /* Copy the text inside the text field */
  document.execCommand("copy");
} 
</script>