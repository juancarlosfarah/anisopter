<!DOCTYPE html>
<html>
% include('head.tpl', title="Upload Animation Background")
<body>
% include('header.tpl')
<div class="container">
    <h2>Upload Animation Background</h2>
    <form action="/target_animation/background/upload"
          method="post"
          enctype="multipart/form-data">
        <div class="form-group">
            <label for="description">Description</label>
            <textarea class="form-control" rows="3" id="description"
                      placeholder="Description" name="description"></textarea>
        </div>
        <div class="form-group">
            <label for="upload">File Input</label>
            <input type="file" id="upload" name="upload"
                   accept="image/png, image/jpeg">
            <p class="help-block">
                Upload a file to use as a background for your animations.
            </p>
        </div>
        <button id="submit" type="submit" class="btn btn-success">Upload</button>
    </form>
</div>
% include('footer.tpl')
</body>
</html>