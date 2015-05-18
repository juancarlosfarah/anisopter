<!DOCTYPE html>
<html>
% include('head.tpl', title="New ESTMD Simulation")
<body>
% include('header.tpl')
<div class="container">
    % include('form_header.tpl', title="New ESTMD Simulation")
    <form action="/estmd/simulation/run" method="post">
        <div class="form-group">
            <label for="sample">Sample</label>
            <select class="form-control" name="sample" id="sample">
                %for s in samples:
                    <option value="{{s['_id']}}">
                        Date: {{s['date']}}
                        Description: {{s['description']}}
                    </option>
                %end
            </select>
        </div>

        <div class="form-group">
            <label for="description">Description</label>
            <textarea class="form-control" rows="3" id="description"
                      placeholder="Description" name="description"></textarea>
        </div>

        <div class="form-group optional">
	    <p> To modify the advanced parameters below, reference should be made to the following paper, from which the implementation is taken: </p>
	    <a href="http://www.researchgate.net/profile/Ben_Cazzolato/publication/233815971_Discrete_implementation_of_biologically_inspired_image_processing_for_target_detection/links/00b7d52d3699b6aa90000000.pdf" target="_blank">Discrete implementation of biologically inspired image processing for target detection</a>
            <br />
	    <p> The H filter is the convolution applied in the photoreceptors: </p>
	    <label for="H_filter">H_filter</label>
            <textarea class="form-control" rows="5" id="H_filter"
                      name="H_filter">
            [[-1, -1, -1, -1, -1],
             [-1,  0,  0,  0, -1],
             [-1,  0,  2,  0, -1],
             [-1,  0,  0,  0, -1],
             [-1, -1, -1, -1, -1]]</textarea>
        </div>

	<p> Below, a and b correspond to the numerator and denominator of the first z-transform: </p>

        <div class="form-group optional">
            <label for="b">b</label>
            <textarea class="form-control" rows="1" id="b"
                      name="b">
            [0.0, 0.00006, -0.00076, 0.0044, -0.016, 0.043, -0.057, 0.1789, -0.1524]</textarea>
        </div>
	
        <div class="form-group optional">
            <label for="a">a</label>
            <textarea class="form-control" rows="1" id="a"
                      name="a">
            [1.0, -4.333, 8.685, -10.71, 9.0, -5.306, 2.145, -0.5418, 0.0651]</textarea>
        </div>

	<p> CSKernel corresponds to the convolution applied in the RTC cell: </p>

        <div class="form-group optional">
            <label for="CSKernel">CSKernel</label>
            <textarea class="form-control" rows="3" id="CSKernel"
                      name="CSKernel">
            [[-1.0 / 9.0, -1.0 / 9.0, -1.0 / 9.0],
             [-1.0 / 9.0,  8.0 / 9.0, -1.0 / 9.0],
             [-1.0 / 9.0, -1.0 / 9.0, -1.0 / 9.0]]</textarea>
        </div>

	<p> Below, a1 and b1 correspond to the numerator and denominator of the final z-transform </p>

        <div class="form-group optional">
            <label for="b1">b1</label>
            <textarea class="form-control" rows="1" id="b1"
                      name="b1">
            [1.0, 1.0] </textarea>
        </div>

        <div class="form-group optional">
            <label for="a1">a1</label>
            <textarea class="form-control" rows="1" id="a1"
                      name="a1">
            [51.0, -49.0]</textarea>
        </div>

        <button type="reset"
                class="btn btn-warning">Reset Defaults</button>

        <button id="submit"
                type="submit"
                class="btn btn-success">Run</button>
    </form>
</div>
% include('footer.tpl')
</body>
</html>
