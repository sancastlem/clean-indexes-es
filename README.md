# Clean Indexes to AWS ElasticSearch Service

Lambda function that clean old indexes or maintenance a number of indexes from your ElasticSearch Service.

## Use

1. Zip the file cleanup.py

```bash

zip your_script_zip_name.zip cleanup.py

```
2. Install the requirements to launch correctly the function. **Path is necessary**.

```bash

pip3 install -r requirements.txt -t python/lib/python3.8/site-packages/

```
3. Zip the folder with contains every libraries.

```bash

zip -r your_layer_zip_name.zip python

```

4. Create the layer, uploading the zip generated previously.

5. Create the lambda function, upload the zip generate previously.

You need to setup this options:

### Global Environments

- **endpoint**: the url of your ElasticSearch Service.
- **region**: region where we created our ElasticSearch Service. Need it to AWS credentials request.
- **days**: number of days that you want maintenance indexes in your ElasticSearch Service. Example, *30*.
- **regex**: necessary to exclude other index employing **filter_by_regex**. Empty if you don't use it. Valid values **prefix**, **suffix**, **regex** or **timestring**. Link to the doc [here](https://curator.readthedocs.io/en/latest/filters.html).
- **exclude**: optional variable content used to exclude the name of the index. Empty if you don't use it. Example with one than more prefix, ^(myindexname-|opendistro|.opendistro).*$.

### AWS Cloudwatch Event Bridge

For cron, you need to create a cron job, employing the service AWS Cloudwatch Event Bridge.

### Basic setup

- Change the name for the controller to **cleanup.main**.
- Change timeout to 60.

### Permissions and role

Make sure that your role have access to Cloudwatch, for logging the launch and ES Service, and your lambda function has the permissions to launch the function.

### Runtime

Python 3.8.

6. Deploy, break and fun!
