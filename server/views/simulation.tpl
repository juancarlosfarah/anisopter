<!DOCTYPE html>
<html
<head>
    <title>Simulation</title>
    <script src="/static/jquery.js"></script>
    <link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet"
          media="screen">
</head>
<body>
<header>
    <nav class="navbar navbar-default">
        <div class="container-fluid">
            <div class="navbar-header">
                <a class="navbar-brand" href="/">
                    Home
                </a>
            </div>
        </div>
    </nav>
</header>

<div class="container">
    <h2>General</h2>
    <table class="table">
        <tr>
            <td>Simulation ID</td>
            <td>{{simulation['_id']}}</td>
        </tr>
        <tr>
            <td>Number of Neurons</td>
            <td>{{len(simulation['neurons'])}}</td>
        </tr>
        <tr>
            <td>Number of Afferents</td>
            <td>{{simulation['num_afferents']}}</td>
        </tr>
        <tr>
            <td>Number of Patterns</td>
            <td>{{len(simulation['start_positions'])}}</td>
        </tr>
        <tr>
            <td>Pattern Duration</td>
            <td>{{simulation['pattern_duration']}} ms</td>
        </tr>
        <tr>
            <td>Duration</td>
            <td>{{simulation['duration']}} ms</td>
        </tr>
    </table>

    <h2>Spike Train</h2>
    <div role="tabpanel">

        <!-- Nav Tabs -->
        <ul class="nav nav-tabs nav-justified" role="tablist">
            % for i in range(len(simulation['potential_plots'])):
            <li role="presentation">
                <a href="#p{{i + 1}}" aria-controls="p{{i + 1}}" role="tab"
                   data-toggle="tab">Plot {{i + 1}}</a>
            </li>
            % end
        </ul>

        <!-- Tab Panes -->
        <div class="tab-content">
            % for i in range(len(simulation['potential_plots'])):
            % p_plot = simulation['potential_plots'][i]
            <div role="tabpanel" class="tab-pane" id="p{{i + 1}}">
                {{!p_plot}}
            </div>
            %end
        </div>

    </div>

    <h2>Neurons</h2>
    <div role="tabpanel">

        <!-- Nav Tabs -->
        <ul class="nav nav-tabs nav-justified" role="tablist">
            % for i in range(len(simulation['neurons'])):
            <li role="presentation">
                <a href="#n{{i + 1}}" aria-controls="n{{i + 1}}" role="tab"
                   data-toggle="tab">Neuron {{i + 1}}</a>
            </li>
            % end
        </ul>

        <!-- Tab Panes -->
        <div class="tab-content">
            % for i in range(len(simulation['neurons'])):
            % neuron = simulation['neurons'][i]
            <div role="tabpanel" class="tab-pane" id="n{{i + 1}}">
                {{!neuron['weight_distribution_plot']}}
            </div>
            % end
        </div>

    </div>

</div>
<script src="/static/bootstrap/js/bootstrap.min.js"></script>
<script>
    $(document).ready(function() {
        // Activate first tab.
        $('.nav-tabs').each(function() {
            $(this).find('li:first').addClass("active");
        });
        $('.tab-content').each(function() {
            $(this).find('div:first').addClass("active");
        });
    });
</script>
</body>
</html>