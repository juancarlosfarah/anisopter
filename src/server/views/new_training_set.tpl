<!DOCTYPE html>
<html>
% include('head.tpl', title="New Training set")
<body>
% include('header.tpl')
<div class="container">
    <h2>New Training set</h2>

    <form action="/training/training_sets/generate" method="post">

        <div class="form-group">
            <label for="height">Height</label>
            <div class="input-group">
                <input type="number" class="form-control" id="height"
                       name="height" value="1" max="10"/>
                <span class="input-group-addon">px</span>
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
        var targets = [];
        $('fieldset.target').each(function() {
            var target = {
                "type": $(this).find('.target-type').val(),
                "color": $(this).find('.target-color').val(),
                "size": $(this).find('.target-size').val(),
                "velocity": $(this).find('.target-velocity').val(),
                "start_pos": [
                    $(this).find('.target-start-pos-x').val(),
                    $(this).find('.target-start-pos-y').val()
                ],
                "velocity_vector": [
                    $(this).find('.target-velocity-x').val(),
                    $(this).find('.target-velocity-y').val()
                ]
            };
            targets.push(target);
        });

        $.ajax({
            method: "POST",
            url: "/target_animation/animation/generate",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            data: JSON.stringify({
                "background": $('#background').val(),
                "width": $('#width').val(),
                "height": $('#height').val(),
                "description": $('#description').val(),
                "frames": $('#frames').val(),
                "targets": targets
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
        $('.removeTarget').first().hide();
        $("#addTargets").click(function() {
            // Add form for targets.
            var $targets = $('#targets');
            var html = $targets.children('fieldset.target').last().html();
            var $new_target = $('<fieldset class="target"></fieldset>');
            $targets.append($new_target.html(html));
            var len = $targets.children('fieldset.target').length;
            $('.target_num').last().text(len);
            $('.color-picker').last().colorpicker();
            $('.removeTarget').last().show();
            removeTargetOnClick($('.removeTarget').last());
        });
        removeTargetOnClick($('.removeTarget'));
        submitFormOnClick($('#submit'));
    });
</script>
</body>
</html>
