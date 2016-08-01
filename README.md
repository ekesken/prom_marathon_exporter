# Prometheus Marathon Exporter

Proxy server converting marathon metrics to prometheus metrics.

## Using Docker

You can deploy this exporter using the [ekesken/prom-marathon-exporter](https://registry.hub.docker.com/u/ekesken/prom-marathon-exporter/) Docker image.

For example:

```bash
docker run -d -e MARATHON_METRICS_URL=http://leader.mesos:8080/metrics -p 9099:9099 ekesken/prom-marathon-exporter
# try it
# curl http://localhost:9099/metrics
```

## Deploy on Marathon

You can deploy this exporter on marathon via following curl command:

```bash
curl -XPOST -H 'Content-Type: application/json;' leader.mesos:8080/v2/apps -d '{
  "cpus": 0.01,
  "mem": 100,
  "id": "/prom/marathon-exporter",
  "instances": 1,
  "env": {
    "MARATHON_METRICS_URL": "http://leader.mesos:8080/metrics"
  },
  "container": {
    "type": "DOCKER",
    "docker": {
      "image": "ekesken/prom-marathon-exporter",
      "network": "BRIDGE",
      "privileged": true,
      "portMappings": [{"containerPort": 9099}]
    }
  },
  "healthChecks": [{"protocol": "HTTP", "path": "/metrics"}]
}'
```

## Scrape config on prometheus

A sample prometheus target yaml example if you already have have mesos-dns:

```
  - job_name: 'marathon'
    dns_sd_configs:
      - names: ['_marathon-exporter-prom._tcp.marathon.mesos']
```