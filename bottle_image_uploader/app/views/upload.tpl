<body>
    <div class="container">

    <h3>Image uploader powerd by bottle</h3>
    

      <form class="upload_form" action="/upload/?username={{username}}" method="post" enctype="multipart/form-data">
        <div class="file_field">
            <input class="file-path validate"  name ="category" type="text" placeholder="image category">
            <span><b>Choose an image: </b></span>
            <br>
            <input type="file" name="upload" placeholder=".png .jpg .gif" accept="image/*">
            <input type="submit" value="Upload">
        </div>
      </form>
    </div>
    <footer> loged in as {{username}} </footer>
</html>