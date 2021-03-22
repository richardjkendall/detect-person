import json
import numpy as np
import cv2
import imutils
import boto3
import os

# setup common things we will use later
s3 = boto3.client("s3")
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# get environment variables we need
target_bucket = os.getenv("OUTPUT_BUCKET")
target_key = os.getenv("OUTPUT_KEY")

def detect_person(bucket, key):
    """
    Called for each s3 put record we get
    """
    s3.download_file(bucket, key, "/tmp/image.jpg")
    img = cv2.imread("/tmp/image.jpg")
    img = imutils.resize(img, width=min(800, img.shape[1]))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(gray, winStride=(4,4), padding=(8,8), scale=1.05)

    if len(boxes) > 0:
        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    
        for (xA, yA, xB, yB) in boxes:
            # display the detected boxes in the colour picture
            cv2.rectangle(img, (xA, yA), (xB, yB),
            (0, 255, 0), 2)
        
        key_parts = key.split("/")
        filename = key_parts[-1]
        cv2.imwrite(f"/tmp/{filename}", img)
        s3.upload_file(f"/tmp/{filename}", target_bucket, f"{target_key}/{filename}")
        return True
    else:
        return False

def lambda_handler(event, context):
    detected_count = 0
    total_count = len(event["Records"])
    for record in event["Records"]:
        details = record["s3"]
        bucket = details["bucket"]["name"]
        key = details["object"]["key"]
        found = detect_person(
            bucket = bucket,
            key = key
        )
        if found:
            detected_count = detected_count + 1
    return {
        "statusCode": 200,
        "body": json.dumps(f"Processed {total_count} records, found {detected_count} that contain people")
    }
