# A Simple Web Application

<!-- toc -->

- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Assumptions](#assumptions)
- [Deployment](#deployment)
- [Resources](#resources)

<!-- tocstop -->

### Introduction

This is a very simple web application for displaying events and their recommendations.  It is based on the [Text-Heavy Website template](https://code.getmdl.io/1.3.0/mdl-template-text-only.zip) of [Material Design Lite](https://getmdl.io/) with [AngularJS](https://angularjs.org/) as the website engine.

### Getting Started

The files here call a RESTful endpoint but can be served locally.  To do so, just execute

```bash
$ python -m SimpleHTTPServer 8000
```

in this directory and you should be able to visit [`http://localhost:8000/`](http://localhost:8000/) from your browers and watch things in action.

### Assumptions

As it stands, the code in [`recengine.js`](recengine.js) will query an AWS API Gateway endpoint looking for a single event.  If you set up your API Gateway to call [the example Lambda function](../code/get_event_from_dynamodb.py) it should work reasonably well.

[`recengine.js`](recengine.js) assumes that in each returned `event` object there is a `recommendation` attribute containing a list of event ids.  You will likely want to modify this behavior to suit your needs.

### Deployment

Once you get your web application working locally, just upload the files to an S3 bucket set for static website hosting.  [This tutorial](https://aws.amazon.com/getting-started/projects/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/) explains how to do that.

### Resources

   * [Material Design Lite](https://getmdl.io/)
   * Material Design Lite [Templates](https://getmdl.io/templates/index.html)
   * [AngularJS](https://angularjs.org/)
   * [AWS API Gateway](https://aws.amazon.com/api-gateway/)
   * [Lambda + DynamoDB + API Gateway tutorial](https://aws.amazon.com/getting-started/projects/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/)
