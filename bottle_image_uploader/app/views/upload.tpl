<style>
  body {
  font-size: 2rem; 
  font-family: 'Roboto', sans-serif;
  background-color: #d4d4d4; 
  padding-left: 33%
}
input[type=text] {
  padding: 10px 32px;
  width: 250px; /* When specifying this, you can use both px and % */
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

</style>


<body>
    <div class="container">

    <h2>Image uploader powerd by bottle</h2>
    <h4>Current size limit @ 12MB </h4>

      <form class="upload_form" action="/upload/" method="post" enctype="multipart/form-data">
        <div class="file_field">
            <input type="text" name="category" placeholder="Add a Category"> <br>
            <input type="file" name="upload" placeholder="suport for .png .jpg .gif" accept="image/*">
            <br>
            <input type="submit" value="Send">
        </div>
      </form>
    </div>
    <footer>  </footer>
</html>