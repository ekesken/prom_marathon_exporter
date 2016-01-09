# Prometheus Marathon exporter

Proxy server converting marathon metrics to prometheus.

## Using Docker

You can deploy this exporter using the [ekesken/prom-marathon-exporter](https://registry.hub.docker.com/u/ekesken/prom-marathon-exporter/) Docker image.

For example:

```bash
docker run -d -p 9100:9100 --net="host" prom/node-exporter
docker run -d -e MARATHON_METRICS_URL=http://leader.mesos:8080/metrics -p 9099:9099 ekesken/prom-marathon-exporter
# try it
# curl http://localhost:9099/metrics
```

