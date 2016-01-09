import logging
import requests
from prometheus_client.core import GaugeMetricFamily,\
    CounterMetricFamily, SummaryMetricFamily


LOGGER = logging.getLogger(__name__)


class SummaryWithQuantileMetricFamily(SummaryMetricFamily):

    def add_quantile(self, quantile, value):
        self.samples.append((self.name, {'quantile': quantile}, value))


class MarathonCollector(object):

    def __init__(self, marathon_metrics_url=None):
        self.marathon_metrics_url = marathon_metrics_url

    def collect(self):
        marathon_metrics_all = self.get_marathon_metrics()
        for metric_type, marathon_metrics in marathon_metrics_all.iteritems():
            if metric_type == 'version':
                continue
            for marathon_key, marathon_metric in marathon_metrics.iteritems():
                if metric_type == 'gauges':
                    yield self.convert_gauge_metric(marathon_key, marathon_metric)
                elif metric_type == 'counters':
                    yield self.convert_counter_metric(marathon_key, marathon_metric)
                elif metric_type == 'histograms':
                    yield self.convert_histogram_metric(marathon_key, marathon_metric)
                elif metric_type == 'meters':
                    yield self.convert_meter_metric(marathon_key, marathon_metric)
                elif metric_type == 'timers':
                    for converted_metric in self.convert_timer_metric(
                            marathon_key, marathon_metric):
                        yield converted_metric
                else:
                    LOGGER.warn(
                            'Unexpected metric type from marathon: %s',
                            metric_type)

    def get_marathon_metrics(self):
        headers = {'Content-Type': 'application/json'}
        connection = requests.get(self.marathon_metrics_url, headers=headers)
        if connection.status_code == 200:
            marathon_metrics = connection.json()
            return marathon_metrics
        else:
            LOGGER.warn()
            return {}

    @staticmethod
    def convert_metric_key(marathon_key):
        key = 'marathon_%s' % marathon_key
        key = key.lower().replace('.', '_').replace('-', '_').replace('$', '_')
        return key

    @classmethod
    def convert_gauge_metric(cls, marathon_key, marathon_metric):
        metric_key = cls.convert_metric_key(marathon_key)
        return GaugeMetricFamily(
            name=metric_key,
            documentation='from %s' % marathon_key,
            value=marathon_metric['value']
        )

    @classmethod
    def convert_counter_metric(cls, marathon_key, marathon_metric):
        metric_key = cls.convert_metric_key(marathon_key)
        c = CounterMetricFamily(
                name=metric_key,
                documentation='from %s' % marathon_key,
                value=marathon_metric['count'])
        return c

    @classmethod
    def convert_histogram_metric(cls, marathon_key, marathon_metric):
        metric_key = cls.convert_metric_key(marathon_key)
        count = int(marathon_metric['count'])
        sum = count * float(marathon_metric['mean'])
        s = SummaryWithQuantileMetricFamily(
            name=metric_key,
            documentation='from %s' % marathon_key,
            count_value=count,
            sum_value=sum,
        )
        for key, value in marathon_metric.iteritems():
            if key.startswith('p'):
                quantile = float('0.%s' % key[1:])
                s.add_quantile(
                   quantile=str(quantile),
                   value=value,
                )
        return s

    @classmethod
    def convert_meter_metric(cls, marathon_key, marathon_metric):
        metric_key = cls.convert_metric_key(marathon_key)
        metric_key = '%s_rate' % metric_key
        g = GaugeMetricFamily(
            name=metric_key,
            documentation='from %s' % marathon_key,
            labels=('window',))
        g.add_metric(('1m',), marathon_metric['m1_rate'])
        g.add_metric(('5m',), marathon_metric['m5_rate'])
        g.add_metric(('15m',), marathon_metric['m15_rate'])
        g.add_metric(('mean',), marathon_metric['mean_rate'])
        return g

    @classmethod
    def convert_timer_metric(cls, marathon_key, marathon_metric):
        meter_part = cls.convert_meter_metric(
                marathon_key, marathon_metric)
        histogram_part = cls.convert_histogram_metric(marathon_key, marathon_metric)
        return meter_part, histogram_part
