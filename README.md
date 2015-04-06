AWS monitoring prototype
========================

Create boto credentials file `~/.boto`

```
[Credentials]
aws_access_key_id = YOUR_KEY
aws_secret_access_key = YourAWSSecret
```

And run

```
virtualenv ENV
source ./ENV/bin/activate
pip install -r ./requirements.txt
gunicorn monitor:app
```

and navigate to http://127.0.0.1:8000/

TODO
----

* Tests
* Proper chart refreshing
* Caching
* More metrics
* Uniform API
* Analytics
* Alerts
