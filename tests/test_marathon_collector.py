import unittest
from collector import MarathonCollector
from prometheus_client import generate_latest


class TestMarathonCollector(unittest.TestCase):

    def setUp(self):
        self.marathon_collector = MarathonCollector('')

        def generate_mock_metrics():
            return {
              "version": "3.0.0",
              "gauges": {
                "org.eclipse.jetty.servlet.ServletContextHandler.percent-4xx-15m": {
                  "value": 0.01139209265037441
                }
              },
              "counters": {
                "org.eclipse.jetty.servlet.ServletContextHandler.active-dispatches": {
                  "count": 1
                }
              },
              "histograms": {
                "service.mesosphere.marathon.state.MarathonStore.AppDefinition.read-data-size": {
                  "count": 1870979,
                  "max": 1732,
                  "mean": 1199.741604950901,
                  "min": 271,
                  "p50": 1231,
                  "p75": 1516,
                  "p95": 1557,
                  "p98": 1558,
                  "p99": 1558,
                  "p999": 1732,
                  "stddev": 306.795816869835,
                }
              },
              "meters": {
                "mesosphere.marathon.state.AppRepository.read-request-errors": {
                  "count": 100,
                  "m15_rate": 15,
                  "m1_rate": 7,
                  "m5_rate": 3,
                  "mean_rate": 7,
                  "units": "events/second"
                }
              },
              "timers": {
                "mesosphere.marathon.api.v2.AppTasksResource$$EnhancerByGuice$$bd9fb6d1.indexJson": {
                  "count": 1870979,
                  "max": 1732,
                  "mean": 1199.741604950901,
                  "min": 271,
                  "p50": 1231,
                  "p75": 1516,
                  "p95": 1557,
                  "p98": 1558,
                  "p99": 1558,
                  "p999": 1732,
                  "m15_rate": 15,
                  "m1_rate": 7,
                  "m5_rate": 3,
                  "mean_rate": 7,
                  "duration_units": "seconds",
                  "rate_units": "calls/second"
                }
              }
            }

        self.marathon_collector.get_marathon_metrics = generate_mock_metrics

    def test_collect(self):
        # used generate_latest method for easy assert
        prom_metrics_text = generate_latest(self.marathon_collector)
        expected_text = '''# HELP marathon_org_eclipse_jetty_servlet_servletcontexthandler_percent_4xx_15m from org.eclipse.jetty.servlet.ServletContextHandler.percent-4xx-15m
# TYPE marathon_org_eclipse_jetty_servlet_servletcontexthandler_percent_4xx_15m gauge
marathon_org_eclipse_jetty_servlet_servletcontexthandler_percent_4xx_15m 0.01139209265037441
# HELP marathon_service_mesosphere_marathon_state_marathonstore_appdefinition_read_data_size from service.mesosphere.marathon.state.MarathonStore.AppDefinition.read-data-size
# TYPE marathon_service_mesosphere_marathon_state_marathonstore_appdefinition_read_data_size summary
marathon_service_mesosphere_marathon_state_marathonstore_appdefinition_read_data_size_count 1870979.0
marathon_service_mesosphere_marathon_state_marathonstore_appdefinition_read_data_size_sum 2244691348.289432
marathon_service_mesosphere_marathon_state_marathonstore_appdefinition_read_data_size{quantile="0.98"} 1558.0
marathon_service_mesosphere_marathon_state_marathonstore_appdefinition_read_data_size{quantile="0.99"} 1558.0
marathon_service_mesosphere_marathon_state_marathonstore_appdefinition_read_data_size{quantile="0.75"} 1516.0
marathon_service_mesosphere_marathon_state_marathonstore_appdefinition_read_data_size{quantile="0.95"} 1557.0
marathon_service_mesosphere_marathon_state_marathonstore_appdefinition_read_data_size{quantile="0.5"} 1231.0
marathon_service_mesosphere_marathon_state_marathonstore_appdefinition_read_data_size{quantile="0.999"} 1732.0
# HELP marathon_mesosphere_marathon_state_apprepository_read_request_errors_rate from mesosphere.marathon.state.AppRepository.read-request-errors
# TYPE marathon_mesosphere_marathon_state_apprepository_read_request_errors_rate gauge
marathon_mesosphere_marathon_state_apprepository_read_request_errors_rate{window="1m"} 7.0
marathon_mesosphere_marathon_state_apprepository_read_request_errors_rate{window="5m"} 3.0
marathon_mesosphere_marathon_state_apprepository_read_request_errors_rate{window="15m"} 15.0
marathon_mesosphere_marathon_state_apprepository_read_request_errors_rate{window="mean"} 7.0
# HELP marathon_mesosphere_marathon_api_v2_apptasksresource__enhancerbyguice__bd9fb6d1_indexjson_rate from mesosphere.marathon.api.v2.AppTasksResource$$EnhancerByGuice$$bd9fb6d1.indexJson
# TYPE marathon_mesosphere_marathon_api_v2_apptasksresource__enhancerbyguice__bd9fb6d1_indexjson_rate gauge
marathon_mesosphere_marathon_api_v2_apptasksresource__enhancerbyguice__bd9fb6d1_indexjson_rate{window="1m"} 7.0
marathon_mesosphere_marathon_api_v2_apptasksresource__enhancerbyguice__bd9fb6d1_indexjson_rate{window="5m"} 3.0
marathon_mesosphere_marathon_api_v2_apptasksresource__enhancerbyguice__bd9fb6d1_indexjson_rate{window="15m"} 15.0
marathon_mesosphere_marathon_api_v2_apptasksresource__enhancerbyguice__bd9fb6d1_indexjson_rate{window="mean"} 7.0
# HELP marathon_mesosphere_marathon_api_v2_apptasksresource__enhancerbyguice__bd9fb6d1_indexjson from mesosphere.marathon.api.v2.AppTasksResource$$EnhancerByGuice$$bd9fb6d1.indexJson
# TYPE marathon_mesosphere_marathon_api_v2_apptasksresource__enhancerbyguice__bd9fb6d1_indexjson summary
marathon_mesosphere_marathon_api_v2_apptasksresource__enhancerbyguice__bd9fb6d1_indexjson_count 1870979.0
marathon_mesosphere_marathon_api_v2_apptasksresource__enhancerbyguice__bd9fb6d1_indexjson_sum 2244691348.289432
marathon_mesosphere_marathon_api_v2_apptasksresource__enhancerbyguice__bd9fb6d1_indexjson{quantile="0.98"} 1558.0
marathon_mesosphere_marathon_api_v2_apptasksresource__enhancerbyguice__bd9fb6d1_indexjson{quantile="0.75"} 1516.0
marathon_mesosphere_marathon_api_v2_apptasksresource__enhancerbyguice__bd9fb6d1_indexjson{quantile="0.99"} 1558.0
marathon_mesosphere_marathon_api_v2_apptasksresource__enhancerbyguice__bd9fb6d1_indexjson{quantile="0.95"} 1557.0
marathon_mesosphere_marathon_api_v2_apptasksresource__enhancerbyguice__bd9fb6d1_indexjson{quantile="0.999"} 1732.0
marathon_mesosphere_marathon_api_v2_apptasksresource__enhancerbyguice__bd9fb6d1_indexjson{quantile="0.5"} 1231.0
# HELP marathon_org_eclipse_jetty_servlet_servletcontexthandler_active_dispatches from org.eclipse.jetty.servlet.ServletContextHandler.active-dispatches
# TYPE marathon_org_eclipse_jetty_servlet_servletcontexthandler_active_dispatches counter
marathon_org_eclipse_jetty_servlet_servletcontexthandler_active_dispatches 1.0
'''
        self.assertEqual(expected_text, prom_metrics_text)

if __name__ == '__main__':
    unittest.main()
