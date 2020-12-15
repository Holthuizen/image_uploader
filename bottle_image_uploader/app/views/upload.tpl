<body>
    <div class="container">

    <h3>Image uploader powerd by bottle</h3>
    

      <form class="upload_form" action="/upload/" method="post" enctype="multipart/form-data">
        <div class="file_field">
            <span><b>Add a Category tage: </b></span>
            <input type="text" name="category" placeholder="default">
            <br>
            <span><b>Choose an image: </b></span>
            <br>
            <input type="file" name="upload" placeholder=".png .jpg .gif" accept="image/*">
            <input type="submit" value="Upload">
        </div>
      </form>
    </div>
    <footer> - </footer>
</html>