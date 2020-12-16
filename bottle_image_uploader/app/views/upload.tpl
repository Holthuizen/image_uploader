<style>
  body {background-color: #d4d4d4; padding-left: 33%}
  
  img {max-width:900px; height: auto}

</style>


<body>
    <div class="container">

    <h3>Image uploader powerd by bottle</h3>
    

      <form class="upload_form" action="/upload/" method="post" enctype="multipart/form-data">
        <div class="file_field">
            <input type="text" name="category" placeholder="Add a Category">
            <input type="file" name="upload" placeholder="suport for .png .jpg .gif" accept="image/*">
            <br>
            <input type="submit" value="Send">
        </div>
      </form>
    </div>
    <footer> - </footer>
</html>