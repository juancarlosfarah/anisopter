<footer></footer>
<div id="LoadingAnimation">
    <img class="bxg-img-64"
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
    })
</script>