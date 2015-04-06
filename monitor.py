import json
import datetime
import math

import falcon
import boto.ec2.cloudwatch


class CPULoadResource(object):
    def on_get(self, req, resp):
        data = []

        c = boto.ec2.cloudwatch.connect_to_region('us-east-1')
        metrics = c.list_metrics()
        cpu_metrics = filter(lambda m: m.name == 'CPUUtilization', metrics)

        end = datetime.datetime.utcnow()
        start = end - datetime.timedelta(0, 300)  # 5 minutes ago

        for cpu_metric in cpu_metrics:
            if 'InstanceId' not in cpu_metric.dimensions:
                continue

            instance = cpu_metric.dimensions['InstanceId'][0]
            result = cpu_metric.query(start, end, 'Average', 'Percent')
            if len(result):
                avg_metric = sum([r['Average'] for r in result]) / len(result)
                data.append({'instance': instance, 'cpu': avg_metric})
            else:
                data.append({'instance': instance, 'cpu': 0})

        resp.body = json.dumps(data)
        resp.content_type = 'application/json'


class IndexResource(object):
    def on_get(self, req, resp):
        resp.body = open('index.html').read()
        resp.content_type = 'text/html'


app = falcon.API()

cpu = CPULoadResource()
app.add_route('/cpu', cpu)

home = IndexResource()
app.add_route('/', home)
