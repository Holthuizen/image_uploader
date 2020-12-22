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

footer{
  font-size: 0.8rem; 
}
input[type=text] {
  padding: 10px 32px;
  width: 20rem; /* When specifying this, you can use both px and % */
  font-size: 16px;
  border: none;
}

input[type=submit] {
  background-color: #4CAF50; /* Green */
  border: none;
  color: white;
  margin-top: 0.5rem; 
  padding: 15px 32px;
  width: 20rem; /* When specifying this, you can use both px and % */
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
}

input[type=file] {
  background-color: #d4d4d4; /* Grey */
  border: 1px black;
  margin-top: 0.5rem; 
  width: 20rem; /* When specifying this, you can use both px and % */
  color: black;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
}

input[type=button] {
  background-color: #d4d4d4; 
  color: black;
  border: none;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 1.5rem;
}

#error_msg{
  color:red;
}

</style>


<body>
    <div class="container">
    <h4>
      Image Share Service. powered by bottle.py <br>
      File size limit @ 24MB. 
      Simply upload a photo you like to share and copy the url. 
    </h4>
    <hr>
      <b id="error_msg">{{msg}}</b>
      <form class="upload_form" action="/upload/" method="post" enctype="multipart/form-data">
        <div class="file_field">
            <input type="text" name="category" placeholder="Add a Category"> <br>
            <input type="file" name="upload" placeholder="suport for .webp .png .jpg .gif and .dmp" accept="image/*">
            <br>
            <input type="submit" value="Send">
        </div>
      </form>
    </div>
    <br>
    <br>
    <input type="button" id="list" onclick="location.href='{{list_url}}';" value="View list of Categorys" /> 


  <br>
  <br>

  </body>
    <footer> <i> disclaimer: When using this service you are responsible for your own uploaded content: Images or other files. only upload files you own or that you have permission to share</i> </footer>
</html>