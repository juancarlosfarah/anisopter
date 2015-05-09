<!DOCTYPE html>
<html>
% include('head.tpl', title="New Animation")
<body>
% include('header.tpl')
<div class="container">
    <h2>New Animation</h2>

    <form action="/target_animation/animation/generate" method="post">
        <div class="form-group">
            <label for="width">Width</label>
            <div class="input-group">
                <input type="number" class="form-control" id="width"
                       name="duration" value="640" max="1000"
                       disabled="disabled" />
                <span class="input-group-addon">px</span>
            </div>
        </div>
        <div class="form-group">
            <label for="num_neurons">Height</label>
            <div class="input-group">
              <input type="number" class="form-control" id="height"
                     name="height" value="480" max="1000"
                     disabled="disabled" />
              <span class="input-group-addon">px</span>
            </div>
        </div>
        <div class="form-group">
            <label for="description">Description</label>
            <textarea class="form-control" rows="3" id="description"
                      placeholder="Description" name="description"></textarea>
        </div>
        <hr>
        <div id="targets">
            <h3>Targets</h3>
            <fieldset class="target">
                <div class="row">
                    <div class="col-md-11">
                        <h4>Target <span class="target_num">1</span></h4>
                    </div>
                    <div class="col-md-1">
                        <button type="button"
                                class="btn btn-xs btn-danger removeTarget">
                            Remove
                        </button>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
                        <div class="form-group">
                            <label>Type</label>
                            <select class="target-type form-control">
                                <option value="0">Stationary</option>
                                <option value="1">Random Movement</option>
                                <option value="2">Straight Movement</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
                        <div class="form-group">
                            <label>Colour</label>
                            <div class="input-group color-picker">
                                <input type="text"
                                       class="target-color form-control"
                                       value="rgb(0,0,0)" placeholder="" />
                                <span class="input-group-addon"><i></i></span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
                        <div class="form-group">
                            <label>Start Position</label>
                            <div class="input-group">
                                <input type="text"
                                       class="target-start-pos-x form-control"
                                       value="" placeholder="" />
                                <span class="input-group-addon">x</span>
                            </div>
                            <div class="input-group">
                                <input type="text"
                                       class="target-start-pos-y form-control"
                                       value="" placeholder="" />
                                <span class="input-group-addon">y</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
                        <div class="form-group">
                            <label>End Position</label>
                            <div class="input-group">
                                <input type="text"
                                       class="target-end-pos-x form-control"
                                       value="" placeholder="" />
                                <span class="input-group-addon">x</span>
                            </div>
                            <div class="input-group">
                                <input type="text"
                                       class="target-end-pos-y form-control"
                                       value="" placeholder="" />
                                <span class="input-group-addon">y</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
                        <div class="form-group">
                            <label>Size</label>
                            <div class="input-group">
                                <input type="text"
                                       class="target-size form-control"
                                       value="" placeholder="10" />
                                <span class="input-group-addon">px</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
                        <div class="form-group">
                            <label>Velocity</label>
                            <div class="input-group">
                                <input type="text"
                                       class="target-velocity form-control"
                                       value="" placeholder="" />
                                <span class="input-group-addon">px/s</span>
                            </div>
                        </div>
                    </div>
                </div>
            </fieldset>
        </div>
        <button type="button"
                id="addTargets"
                class="btn btn-primary">Add Target</button>
        <button type="button"
                class="btn btn-success btn-default"
                id="submit">Submit</button>
    </form>
</div>
<script src="/static/bootstrap-colorpicker/js/bootstrap-colorpicker.min.js">
</script>
<script>
    function removeTargetOnClick($element) {
        var $targets = $('#targets');
        $element.click(function() {
            if ($targets.children('fieldset.target').length > 1) {
                $(this).closest('fieldset.target').remove();
            }
        });
    }

    function submitForm() {
        var targets = [];
        $('fieldset.target').each(function() {
            var target = {
                "type": $(this).find('.target-type').val(),
                "color": $(this).find('.target-color').val(),
                "start_pos": [
                    $(this).find('.target-start-pos-x').val(),
                    $(this).find('.target-start-pos-y').val()
                ],
                "end_pos": [
                    $(this).find('.target-end-pos-x').val(),
                    $(this).find('.target-end-pos-y').val()
                ],
                "size": $(this).find('.target-size').val(),
                "velocity": $(this).find('.target-velocity').val()
            };
            targets.append(target);
        });

        $.ajax({
            method: "POST",
            url: "/target_animation/animation/generate",
            data: {
                "width": $('#width').val(),
                "height": $('#height').val(),
                "description": $('#description').val(),
                "target": targets
            }
        }).done(function(msg) {
            console.log( "Data Saved: " + msg );
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
