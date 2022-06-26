# ProgImage.com
## API for image storage and processing

Image File Upload
- support bulk uploading
- image can be supplied as data in POST request
- as remote image via URL
- images already in repository

Image File Retrieval

Image Transformation
- compression
- rotation
- a variety of filters
- thumbnail creation
- masking


## Requirements
1. Build a simple service that can receive an uploaded image and return a unique
identifier for the uploaded image that can be used subsequently to retrieve the
image.
2. Extend the service so that different image formats can be returned by using a
different image file type as an extension on the image request URL.
3. Write a series of automated tests that test the image upload, download and file
format conversion capabilities.

## Out of scope
1. The service should be functional but does not need to be production-ready.
2. You do not need to handle input validation and error cases.
3. Your service can run locally. It does not need to be deployed anywhere.

## Questions we will ask
1. What technology choices did you select to implement the service? Why?
2. What would you want to add to your service before deploying and operating it in a
production environment?
3. How would your service handle load at scale?
4. How would you extend the service to handle different image transformation types
e.g. rotations, resizing?
5. What testing did (or would) you do, and why?
6. What would you have done if you had to do this in 1/3 of the time?
