import boto3
import json


def lambda_handler(event: dict, _: dict) -> dict:
    """Retrieve image from S3, analyze it using Rekognition
    and generate a JSON report with the image labels

    Args:
        event (dict): the source event
        context (dict): the source context

    Returns:
        dict: the main image tags, and a status code
    """
    # Retrieve images informations
    images = (
    {
        # Retrieve the bucket name from the incoming request
        "bucket": b["s3"]["bucket"]["name"],
        # Retrieve the file name (with the path) from the incoming request
        "object": b["s3"]["object"]["key"]
    }   for b in event["Records"])
    
    return {
        "status": 200,
        "message": {
            "status": "Ok",
            "generated_files": process_images(images)
        }
    }


def process_images(images: list) -> list:
    """Process each images in the list and return
    a list of generated files

    Args:
        images (list): the list of new images to analyze

    Returns:
        list: the list of generated files
    """
    # Declare the Amazon Rekognition client to use
    rekognition_client = boto3.client("rekognition")
    # Declare the Amazon S3 client to use
    s3 = boto3.resource("s3")
    # Store generated files into a list
    generated_files = []
    # Process each images
    for image in images:
        # Detect celebrities of the input image
        rekognition_response = rekognition_client.recognize_celebrities(
            Image = {
                "S3Object": {
                    "Bucket": image["bucket"],
                    "Name": image["object"],
                },
            },
        )
        # Generate a new filename for the JSON file
        json_filename = f"{image['object'].removesuffix('.jpg')}.json"
        # Initialize the JSON object to write
        s3_object = s3.Object(image["bucket"], json_filename)
        # Write the object to the S3 Bucket
        s3_object.put(
            Body=(bytes(json.dumps(rekognition_response, indent=4).encode("UTF-8")))
        )
        # Add the JSON file to the generated_files list
        generated_files.append(
            f"{image['bucket']}/{json_filename}"
        )
    # Return the list of generated files
    return generated_files
