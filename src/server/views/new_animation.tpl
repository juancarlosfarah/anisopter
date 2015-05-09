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
        <div class="form-group">
            <label for="num_targets">Number of Targets</label>
            <input type="number" class="form-control"
                   name="num_targets" placeholder="1" id="num_targets" />
        </div>
        <hr>
        <div id="targets">
            <h3>Targets</h3>
            <fieldset class="target">
                <div class="row">
                    <div class="col-md-10">
                        <legend class="h4">
                            Target <span class="target_num">1</span>
                        </legend>
                    </div>
                    <div class="col-md-2">
                        <span class="glyphicon glyphicon-remove"></span>
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
                class="btn btn-primary">Add Targets</button>
        <button type="submit" class="btn btn-default">Submit</button>
    </form>
</div>
<script src="/static/bootstrap-colorpicker/js/bootstrap-colorpicker.min.js">
</script>
<script>
    function removeTargetOnClick($element) {
        $element.click(function() {
            if ($targets.children('fieldset.target').length > 1) {
                $(this).closest('fieldset.target').remove();
            }
        });
    }

    $(document).ready(function() {
        $('.color-picker').colorpicker();
        $("#addTargets").click(function() {
            // Add form for targets.
            var $targets = $('#targets');
            var html = $targets.children('fieldset.target').last().html();
            $targets.append(html);
            $('.color-picker').last().colorpicker();
            removeTargetOnClick($('.glyphicon-remove').last());
        });
        removeTargetOnClick($('.glyphicon-remove')); 
    });
</script>
</body>
</html>
