<!DOCTYPE html>
<html>
% include('head.tpl', title="New Animation")
<body>
% include('header.tpl')
<div class="container">
    % include('form_header.tpl', title="New Animation")
    <form action="/target_animation/animation/generate" method="post">
        <div class="form-group">
            <label for="background">Background</label>
            <select class="target-type form-control"
                    name="background"
                    id="background">
                <option value="">None</option>
                %for bg in bgs:
                <option value="{{bg['_id']}}{{bg['extension']}}">
                    Date: {{bg['date']}}
                    Description: {{bg['description']}}
                </option>
                %end
            </select>
        </div>
	    <div class="form-group">
            <label for="background_speed">Background Speed</label>
            <div class="input-group">
                <input type="number" class="form-control" id="background_speed"
                       name="background_speed" value="0" />
                <span class="input-group-addon">px/frame</span>
            </div>
        </div>
        <div class="form-group optional">
            <label for="width">Width</label>
            <div class="input-group">
                <input type="number" class="form-control" id="width"
                       name="width" value="640" max="1000"
                       disabled="disabled" />
                <span class="input-group-addon">px</span>
            </div>
        </div>
        <div class="form-group optional">
            <label for="height">Height</label>
            <div class="input-group">
              <input type="number" class="form-control" id="height"
                     name="height" value="480" max="1000"
                     disabled="disabled" />
              <span class="input-group-addon">px</span>
            </div>
        </div>
        <div class="form-group">
            <label for="frames">Number Frames</label>
            <div class="input-group">
                <input type="number" class="form-control" id="frames"
                       name="frames" value="50" min="10" max="500" />
                <span class="input-group-addon">frames</span>
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
                    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-12">
                        <div class="form-group">
                            <label>Type</label>
                            <select class="target-type form-control">
                                <option value="1">Random Movement</option>
                                <option value="2">Straight Movement</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-12">
                        <div class="form-group">
                            <label>Size</label>
                            <div class="input-group">
                                <input type="text"
                                       class="target-size form-control"
                                       value="10" />
                                <span class="input-group-addon">px</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-12">
                        <div class="form-group">
                            <label>Velocity</label>
                            <div class="input-group">
                                <input type="text"
                                       class="target-velocity form-control"
                                       value="5" />
                                <span class="input-group-addon">px/frame</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-3 col-md-3 col-sm-6 col-xs-12">
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
                                       value="320" placeholder="" />
                                <span class="input-group-addon">x</span>
                            </div>
                            <div class="input-group">
                                <input type="text"
                                       class="target-start-pos-y form-control"
                                       value="240" />
                                <span class="input-group-addon">y</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-6 col-md-6 col-sm-6 col-xs-12">
                        <div class="form-group">
                            <label>Velocity Vector</label>
                            <div class="input-group">
                                <input type="text"
                                       class="target-velocity-x form-control"
                                       value="1" />
                                <span class="input-group-addon">x</span>
                            </div>
                            <div class="input-group">
                                <input type="text"
                                       class="target-velocity-y form-control"
                                       value="1" />
                                <span class="input-group-addon">y</span>
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
                class="btn btn-success btn-default ajax-submit"
                id="submit">Submit</button>
    </form>
</div>
% include('footer.tpl')
</body>
</html>
