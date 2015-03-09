<!DOCTYPE html>
<html>
% include('head.tpl', title="Simulation")
<body>
% include('header.tpl')
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
                <h3>Properties</h3>
                <table class="table">
                    <tr>
                        <td>Theta</td>
                        <td>{{neuron['theta']}}</td>
                    </tr>
                    <tr>
                        <td>Alpha</td>
                        <td>{{neuron['alpha']}}</td>
                    </tr>
                </table>
                <br />
                % if i == 0:
                <h3>Spike Timing Information</h3>
                <table class="table">
                    <tr>
                        <th>Type</th>
                        <th>First Quarter</th>
                        <th>Second Quarter</th>
                        <th>Third Quarter</th>
                        <th>Fourth Quarter</th>
                    </tr>
                    <tr>
                        <td>True Positives</td>
                        <td>{{'%.2f' % neuron['spike_info'][0][0]}}%</td>
                        <td>{{'%.2f' % neuron['spike_info'][1][0]}}%</td>
                        <td>{{'%.2f' % neuron['spike_info'][2][0]}}%</td>
                        <td>{{'%.2f' % neuron['spike_info'][3][0]}}%</td>
                    </tr>
                    <tr>
                        <td>False Positives</td>
                        <td>{{'%.2f' % neuron['spike_info'][0][1]}}%</td>
                        <td>{{'%.2f' % neuron['spike_info'][1][1]}}%</td>
                        <td>{{'%.2f' % neuron['spike_info'][2][1]}}%</td>
                        <td>{{'%.2f' % neuron['spike_info'][3][1]}}%</td>
                    </tr>
                    <tr>
                        <td>False Negatives</td>
                        <td>{{'%.2f' % neuron['spike_info'][0][2]}}%</td>
                        <td>{{'%.2f' % neuron['spike_info'][1][2]}}%</td>
                        <td>{{'%.2f' % neuron['spike_info'][2][2]}}%</td>
                        <td>{{'%.2f' % neuron['spike_info'][3][2]}}%</td>
                    </tr>
                </table>
                <br />
                % end
                {{!neuron['weight_distribution_plot']}}
                <br />
            </div>
            % end
        </div>

    </div>

</div>
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