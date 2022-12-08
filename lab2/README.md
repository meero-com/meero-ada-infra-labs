# Meero x ADA - Lab 2 <!-- omit in toc -->

In this lab, you will learn how to setup a basic image analysis process, using Amazon Lambdas, S3 and Rekognition

- [Code explanation](#code-explanation)
- [Should I modify some files?](#should-i-modify-some-files)
- [Should I add some files?](#should-i-add-some-files)

## Code explanation

The code you will use in your Lambda is pretty simple. Let's take a look at it:

First, we will fetch some informations from the event; because the Lambda will be triggered by a S3 event, you will have a lot of informations about the created objects, so you must keep only useful informations.

```python
# Retrieve images information
images = (
{
    # Retrieve the bucket name from the incoming request
    "bucket": b["s3"]["bucket"]["name"],
    # Retrieve the file name (with the path) from the incoming request
    "object": b["s3"]["object"]["key"]
}   for b in event["Records"])
```

Then, you will process each images from the event by sending their location to Amazon Rekognition. Because S3 is the only resource that will trigger this lambda, we can have some static arguments:

```python
# Detect labels of the input image
rekognition_response = rekognition_client.detect_labels(
    Image = {
        "S3Object": {
            "Bucket": image["bucket"],
            "Name": image["object"],
        }
    }
)
```

Once you have received a response from Rekognition, the program will write the data to a brand new file, and upload it to S3:

```python
# Generate a new filename for the JSON file
json_filename = image["object"].removesuffix(".jpg") + ".json"
# Initialize the JSON object to write
s3_object = s3.Object(image["bucket"], json_filename)
# Write the object to the S3 Bucket
s3_object.put(
    Body=(bytes(json.dumps(rekognition_response, indent=4).encode('UTF-8')))
)
```

Finally, it will add the created file to a list, that will be sent as the program response:

```python
return {
    "status": 200,
    "message": {
        "status": "Ok",
        "generated_files": process_images(images)
    }
}
```

## Should I modify some files?

No, you don't need to modify any of the provided files.

## Should I add some files?

Yes, you do!

Find some `.jpg` images and you should be ready to analyze them where your infrastructure will be ready!

You can also take a look at the [`images`](images) folder to test some images.
