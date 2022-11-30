import boto3
import json

# Define some values that you will use later to analyze your images
maximum_labels_number = 10
minimum_confidence_percentage = 80

def lambda_handler(event: dict, context: dict) -> dict:
    """Retrieve image from S3, analyze it using Rekognition
    and generate a JSON report with the image labels

    Args:
        event (dict): the source event
        context (dict): the source context

    Returns:
        dict: the main image tags, and a status code
    """
    # Declare the Amazon Rekognition client to use
    rekognition_client = boto3.client("rekognition")
    # Declare the Amazon S3 client to use
    s3 = boto3.resource("s3")
    # Store generated files into a list
    generated_files = []

    # Retrieve images informations
    images = (
    {
        # Retrieve the bucket name from the incoming request
        "bucket": b["s3"]["bucket"]["name"],
        # Retrieve the file name (with the path) from the incoming request
        "object": b["s3"]["object"]["key"]
    }   for b in event["Records"])
    
    # Process each images
    for image in images:
        # Detect labels of the input image
        rekognition_response = rekognition_client.detect_labels(
            Image = {
                "S3Object": {
                    "Bucket": image["bucket"],
                    "Name": image["object"],
                }
            },
            MaxLabels=maximum_labels_number,
            MinConfidence=minimum_confidence_percentage,
        )
        # Generate a new filename for the JSON file
        json_filename = image["object"].removesuffix(".jpg") + ".json"
        # Initialize the JSON object to write
        s3_object = s3.Object(image["bucket"], json_filename)
        # Write the object to the S3 Bucket
        s3_object.put(
            Body=(bytes(json.dumps(rekognition_response, indent=4).encode('UTF-8')))
        )
        # Add the JSON file to the generated_files list
        generated_files.append(
            image["bucket"] + json_filename
        )
    
    return {
        "status": 200,
        "message": {
            "status": "Ok",
            "generated_files": generated_files
        }
    }
