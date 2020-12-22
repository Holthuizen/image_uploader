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
        padding-left: 15%; 
    } 
    
    img {max-width:900px; 
        height: auto; 
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

    a { 
        text-decoration: none; 
        color: darkblue;
    }
</style>

<body>
    <input type="button" id="Home" onclick="location.href='{{server}}';" value="#home" /> 
    <hr>
    <br>

    % for item in collection:
        <a href="{{server}}/category/{{item}}">{{item}}</a><br><br>
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