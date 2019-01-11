# LEADIQ Challenge

The goal of this challenge is to build an ​ Imgur​ image uploading service that exposes a REST API.

Clients of this service:
* Submit image upload jobs
    * Each upload job is an array of image URLs. The service takes each URL, downloads the content, and uploads it to Imgur.
* Get the status of an image upload job
    * Every job returns a jobId which can be used to check if the job is completed yet.
    *Returns the lists of image URLs that are still waiting to be processed, were successfully uploaded, and those that failed.
* Get a list of all images uploaded
    * Return a list of Imgur links to all of the images uploaded

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Installing

You need to have Python 2.7 installed in your machine, then you have t build the docker image.
```
cd <project_path>
sudo docker build -t web .
```
In order to run the servers you need.
```
sudo docker-compose up -d --build
```

## Access token

You must have an access token in order to run the test.
In order to register an access token, open the following link, then click on redirect.
```
http://localhost:5004/
```
In case the imgur authorization window appears click on "allow".
If you see "Access Token Acquired", then you are up to go.
### Break down into end to end tests

To run tests try the following command

```
sudo docker-compose run test
```

## Authors

* **Mohamed Zied Arbi** - (medzied.arbi@gmail.com, https://github.com/mzarbi)

