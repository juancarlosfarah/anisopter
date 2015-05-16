<div></div>
<footer class="container-fluid text-center">
    <br />
    <div class="row">
        <div class="col-lg-8 col-offset-2 col-md-8 col-md-offset-2 col-sm-10 col-sm-offset-1 col-xs-12 col-sm-offset-0">
            <div class="row">
                <div class="col-lg-4 col-md-4 col-sm-4 col-xs-4">
                    <a class="h4" href="/target_animation">Target Animation</a>
                </div>
                <div class="col-lg-4 col-md-4 col-sm-4 col-xs-4">
                    <a class="h4" href="/estmd">ESTMD</a>
                </div>
                <div class="col-lg-4 col-md-4 col-sm-4 col-xs-4">
                    <a class="h4" href="/cstmd">CSTMD1</a>
                </div>
            </div>
            <div class="row">
                <div class="col-lg-4 col-md-4 col-sm-4 col-xs-4">
                    <a class="h4" href="/pattern_recognition">Pattern Recognition</a>
                </div>
                <div class="col-lg-4 col-md-4 col-sm-4 col-xs-4">
                    <a class="h4" href="/action_selection">Action Selection</a>
                </div>
                <div class="col-lg-4 col-md-4 col-sm-4 col-xs-4">
                    <a class="h4" href="/training">Training</a>
                </div>
            </div>
        </div>
    </div>
    <br />
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <span class="h6">&copy; 2015 Anisopter LTD</span>
        </div>
    </div>
    <br />
</footer>
<div id="LoadingAnimation">
    <img class="img-responsive"
         src="/assets/images/hexagon-spiral.gif"
         alt="Loading..."/>
</div>
<script>
    /**
     * FUNCTION: positionFooter
     * ========================
     * This function positions the footer at the bottom of the window if the
     * window is larger than the <body> and elongates the body in order to
     * fill the gap between the footer and the body's content. Otherwise it
     * places it within its normal flow.
     */
    function positionFooter() {
        var $footer = $('footer'),
            $body = $('body'),
            $window = $(window);

        $footer.css({ 'position' : 'static', 'bottom' : 'auto', 'width' : 'auto'});
        $body.css({ 'height' : 'auto'});

        if ($body.height() < $window.height()) {
            $footer.css({ 'position' : 'fixed', 'bottom' : 0, 'width' : '100%'});
            $body.height($window.height() - $footer.height());
        }
        $footer.show();
    }

    // This function positions the element in the middle of the browser window.
    function centerElement($element) {
        var $windowWidth = $(window).width();
        var $windowHeight = $(window).height();
        var $elementWidth = $element.outerWidth();
        var $elementHeight = $element.outerHeight();

        $element.css({
            'left': ($windowWidth - $elementWidth) / 2 + 'px',
            'top': ($windowHeight - $elementHeight) / 2 + 'px'
        });
    }

    function showLoader($curtain, $element) {
        if ($curtain instanceof jQuery) {
            $curtain.show();
        }
        centerElement($element);
        $element.fadeIn();
    }

    function removeTargetOnClick($element) {
        var $targets = $('#targets');
        $element.click(function() {
            if ($targets.children('fieldset.target').length > 1) {
                $(this).closest('fieldset.target').remove();
                positionFooter();
            }
        });
    }

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
                "background_speed": $('#background_speed').val(),
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

        $('#submit').click(function() {
            var $curtain = $('.curtain-fade');
            var $animation = $('#LoadingAnimation');
            showLoader($curtain, $animation);
        });
        var $showOptionalFields = $('#showOptionalFields');

        $showOptionalFields.click(function() {
            $('.optional').toggle();
            var text = $(this).text();
            if (text == "Show Advanced Controls") {
                $(this).text("Hide Advanced Controls");
            } else {
                $(this).text("Show Advanced Controls")
            }
            positionFooter();
        });

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
            positionFooter();
        });

        removeTargetOnClick($('.removeTarget'));
        submitFormOnClick($('#submit'));
        positionFooter();
    });

</script>
