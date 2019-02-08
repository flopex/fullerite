import diamond.collector
import json
import urllib2


class OrchestratorCollector(diamond.collector.Collector):

    METRICS_PATH = "debug/metrics"

    ORCHESTRATOR_STATS = [
        'recover.dead_co_master.fail',
        'recover.dead_co_master.start',
        'recover.dead_co_master.success',
        'recover.dead_intermediate_master.fail',
        'recover.dead_intermediate_master.start',
        'recover.dead_intermediate_master.success',
        'recover.dead_master.fail',
        'recover.dead_master.start',
        'recover.dead_master.success',
        'recover.pending'
    ]

    def get_default_config_help(self):
        config_help = super(OrchestratorCollector,
                            self).get_default_config_help()
        config_help.update({
            'host': 'Hostname',
            'port': 'Port (default is 3000)'
        })
        return config_help

    def get_default_config(self):
        config = super(OrchestratorCollector, self).get_default_config()
        config.update({
            'host': 'localhost',
            'port': 3000,
            'path': 'orchestrator'
        })
        return config

    def __init__(self, *args, **kwargs):
        super(OrchestratorCollector, self).__init__(*args, **kwargs)

    def collect(self):
        metrics = self.get_metrics()

        for k, v in metrics.iteritems():
            if k in self.ORCHESTRATOR_STATS:
                self.publish(k, v)

    def get_metrics(self):
        try:
	    url = 'http://%s:%s/%s' % ( self.config['host'],
                                        self.config['port'],
                                        self.METRICS_PATH )
            return json.load(urllib2.urlopen(url))
        except (urllib2.HTTPError, ValueError), err:
            self.log.error('Unable to read JSON response: %s' % err)
            return {}
