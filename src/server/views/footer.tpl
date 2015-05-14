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
        });
        positionFooter();
    })
</script>
