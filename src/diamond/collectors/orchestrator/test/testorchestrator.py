#!/usr/bin/python
# coding=utf-8
################################################################################

from test import CollectorTestCase
from test import get_collector_config
from test import unittest
from mock import Mock
from mock import patch

from diamond.collector import Collector

from orchestrator import OrchestratorCollector

################################################################################


class TestOrchestratorCollector(CollectorTestCase):
    def setUp(self):
        config = get_collector_config('OrchestratorCollector', {})

        self.collector = OrchestratorCollector(config, None)

    def test_import(self):
        self.assertTrue(OrchestratorCollector)

    @patch.object(Collector, 'publish')
    def test_should_work_with_real_data(self, publish_mock):
        def se(url):
            if url == 'http://localhost:3000/debug/metrics':
                return self.getFixture('metrics')

        patch_urlopen = patch('urllib2.urlopen', Mock(side_effect=se))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        metrics = self.get_metrics()
        self.setDocExample(collector=self.collector.__class__.__name__,
                           metrics=metrics,
                           defaultpath=self.collector.config['path'])
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(Collector, 'publish')
    def test_should_fail_gracefully(self, publish_mock):
        patch_urlopen = patch('urllib2.urlopen', Mock(
                              return_value=self.getFixture('metrics_blank')))

        patch_urlopen.start()
        self.collector.collect()
        patch_urlopen.stop()

        self.assertPublishedMany(publish_mock, {})

    def get_metrics(self):
        return {
	    'recover.dead_co_master.fail': 2,
	    'recover.dead_co_master.start': 7,
	    'recover.dead_co_master.success': 5,
	    'recover.dead_intermediate_master.fail': 3,
	    'recover.dead_intermediate_master.start': 9,
	    'recover.dead_intermediate_master.success': 6,
	    'recover.dead_master.fail': 4,
	    'recover.dead_master.start': 11,
	    'recover.dead_master.success': 7,
	    'recover.pending': 2
        }

################################################################################
if __name__ == "__main__":
    unittest.main()
