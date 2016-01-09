#!/bin/bash

sed -i "s/processes=1/processes=$PROCESSES/g" /prom_marathon_exporter/uwsgi.ini
supervisord && uwsgi --ini /prom_marathon_exporter/uwsgi.ini
