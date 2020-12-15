<br>
<h3>Category: {{ category }}</h3>
<body>
    <img src="{{url}}">
    <input id="cb" type="text" hidden>
    <br>
    <input type="text" value="{{short_url}}" id="short_url"> <input type="button" onclick="copy_short_url()" value="#Copy (short) URL" /><br>
    <input type="button" onclick="location.href='{{download_url}}';" value="#Download" /><br>
    <input type="button" onclick="location.href='{{delete_url}}';" value="#Delete" /><br>


    

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

  /* Alert the copied text */
  alert("Copied the text: " + copyText.value);
} 
</script>