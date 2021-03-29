# detect-person
Using opencv to detect people in images uploaded to an S3 bucket.

This is designed to be deployed as a lambda function on AWS, it should be attached to an S3 ObjectCreated:* notification.  For each new image which is uploaded 
to the source bucket it will attempt to find any people in the image using the opencv HOG (histogram of oriented gradients) default people detector.

Where one or more people are detected the function draws a green rectangle around each one and then saves the resulting image in an output S3 bucket using a specific key prefix.

## Environment Variables

OUTPUT_BUCKET = name of the bucket where the resulting images should be saved
OUTPUT_KEY = key prefix to use when saving the resulting images in the output bucket

## Permissions Needed

The lambda function needs to have permissions to access the source bucket and the output bucket.

## Deployment

There is a terraform module available here https://github.com/richardjkendall/tf-modules/tree/master/modules/people-detect-lambda to deploy it.
