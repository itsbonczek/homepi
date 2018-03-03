# homepi


My raspberri pi setup for home automation control via Amazon Alexa. Currently only used to control a Roku-based TV. 

## Overview


This code is a starting point to exposing logical devices to your Amazon Alexa and executing arbitrary code as a response to commands.

Basic workflow:

`Alexa -> AWS Lambda -> AWS IoT -> Raspberry Pi -> Device`


## Code

### aws

The lambda that handles device discovery and request forwarding. You'll need to ensure your lambda has a policy in place that lets it publish messages to AWS IoT endpoints. I used the **AWSIoTDataAccess** managed policy for this.  

`build.sh` will package the lambda up for upload. You'll need to set the handler to lambda_handler.lambda_handler in the AWS lambda console.

### device

The Alexa logical device and core device drivers.

### host

The AWS IoT host. This should be run on the Raspberry Pi. AWS IoT uses SSL for secure communication to the device, which is configured in the host script using the following environment variables:

+ **HOMEPI_IOT_ENDPOINT** - the endpoint of your IOT device
+ **HOMEPI_ROOT_CA_PATH** - the path to the root CA certificate
+ **HOMEPI_PRIVATE_KEY_PATH** - the path to the private key of the device
+ **HOMEPI_CERT_PATH** - the path to the SSL certificate

All of the above should be easy to supply after setting up your IoT device in the AWS console.

### scripts

`build.sh` - runs unit tests and packages the lambda

`bootstrap.sh` - installs dependencies 


## Notes

This code is written in Python 3.6. The Raspberry Pi currently still ships with Python 2.7, so you'll need to build 3.6 from source. I followed this [tutorial](https://gist.github.com/dschep/24aa61672a2092246eaca2824400d37f).

This was a weekend project I built while my son was napping, so please execuse the messy code and lack of documentation. Hopefully it's useful as a starting point. Please reach out if you have any questions! 

