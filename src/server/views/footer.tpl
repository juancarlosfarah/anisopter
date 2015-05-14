<footer class="container-fluid text-center">
    <div class="row bxg-footer-container">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 text-center">
            <div class="row text-left">
                <div class="col-lg-4 col-md-4 col-sm-4 col-xs-4">
                    <a class="h5" href="/target_animation">Target Animation</a>
                </div>
                <div class="col-lg-4 col-md-4 col-sm-4 col-xs-4">
                    <a class="h5" href="/estmd">ESTMD</a>
                </div>
                <div class="col-lg-4 col-md-4 col-sm-4 col-xs-4">
                    <a class="h5" href="/cstmd">CSTMD1</a>
                </div>
            </div>
            <div class="row text-left">
                <div class="col-lg-4 col-md-4 col-sm-4 col-xs-4">
                    <a class="h5" href="/pattern_recognition">
                        Pattern Recognition
                    </a>
                </div>
                <div class="col-lg-4 col-md-4 col-sm-4 col-xs-4">
                    <a class="h5" href="/action_selection">Action Selection</a>
                </div>
                <div class="col-lg-4 col-md-4 col-sm-4 col-xs-4">
                    <a class="h5" href="/training">Training</a>
                </div>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <span class="h6">&copy; 2015 Anisopter LTD</span>
        </div>
    </div>
</footer>
<div id="LoadingAnimation">
    <img class="img-responsive"
         src="/assets/images/hexagon-spiral.gif"
         alt="Loading..."/>
</div>
<script>
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
        $('#showOptionalFields').click(function() {
            $('.optional').toggle();
        });
    })
</script>
