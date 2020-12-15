<style>
body {background-color: #d4d4d4; padding-left: 33%}
img {max-width:900px; height: auto}
</style>
<body>
    % for item in collection:
      <img src="{{item['full_url']}}">
      <br>
      <input type="text" value="{{item['copy_url']}}" id="{{item['copy_url']}}"> <input type="button" onclick="copy_short_url( '{{item['copy_url']}}' )" value="#Copy (short) URL" /> 
      <input type="button" onclick="location.href='{{item['download_url']}}';" value="#Download" /> 
      <input type="button" onclick="location.href='{{item['delete_url']}}';" value="#Delete" /> 
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