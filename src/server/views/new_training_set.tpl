<!DOCTYPE html>
<html>
% include('head.tpl', title="New Training set")
<body>
% include('header.tpl')
<div class="container">
    <h2>New Training set</h2>

    <form action="/training/training_sets/generate" method="post">

        <div class="form-group">
            <label for="repetitions">Test repetitions</label>
            <div class="input-group">
                <input type="number" class="form-control" id="repetitions"
                       name="repetitions" value="10" max="100"/>
                <span class="input-group-addon">reps</span>
            </div>
        </div>

        <div class="form-group">
            <label for="vertical">Vertical tests</label>
            <div class="input-group">
                <input type="number" class="form-control" id="vertical"
                       name="vertical" value="1" max="10"/>
                <span class="input-group-addon">type</span>
            </div>
        </div>

        <div class="form-group">
            <label for="horizontal">Horizontal tests</label>
            <div class="input-group">
                <input type="number" class="form-control" id="horizontal"
                       name="horizontal" value="1" max="10"/>
                <span class="input-group-addon">type</span>
            </div>
        </div>

        <div class="form-group">
            <label for="diagonal">Diagonal tests</label>
            <div class="input-group">
                <input type="number" class="form-control" id="diagonal"
                       name="diagonal" value="1" max="10"/>
                <span class="input-group-addon">type</span>
            </div>
        </div>

        <div class="form-group">
            <label for="anti_diagonal">Anti_diagonal tests</label>
            <div class="input-group">
                <input type="number" class="form-control" id="anti_diagonal"
                       name="anti_diagonal" value="1" max="10"/>
                <span class="input-group-addon">type</span>
            </div>
        </div>


        <button type="button"
                class="btn btn-success btn-default"
                id="submit">Submit</button>
    </form>
</div>
<script src="/static/bootstrap-colorpicker/js/bootstrap-colorpicker.min.js">
</script>
<script>
    function submitForm() {

        $.ajax({
            method: "POST",
            url: "/training/training_sets/generate'",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: JSON.stringify({
                "repetitions": $('#repetitions').val(),
                "vertical": $('#vertical').val(),
                "horizontal": $('#horizontal').val(),
                "diagonal": $('#diagonal').val(),
                "anti_diagonal": $('#anti_diagonal').val()
            })
        }).done(function(data) {
            window.location.href = data.url;
        });
    }

    function submitFormOnClick($element) {
        $element.click(function() {
            console.log("Submitting form...");
            submitForm();
        });
    }

    $(document).ready(function() {
        $('.color-picker').colorpicker();
        submitFormOnClick($('#submit'));
    });
</script>
</body>
</html>
