#!/bin/bash

# This script is used to build the layer for the lambda function
# The layer is used to store the dependencies that are shared across multiple lambda functions
# The layer is built and pushed to ECR

# to give permission to the script (run this the first time)
# chmod +x build_layer.sh
# to run the script
# ./build_layer.sh

# as per ECR documentation, we need to login first
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 471112589532.dkr.ecr.us-east-1.amazonaws.com

docker build -t nba_layer -f layer.Dockerfile .

docker tag nba_layer:latest 471112589532.dkr.ecr.us-east-1.amazonaws.com/nba_layer:latest

docker push 471112589532.dkr.ecr.us-east-1.amazonaws.com/nba_layer:latest

# run the lambda_function/build_lambda.sh script to deploy the lambda function
./build_lambda.sh

# TO GO INTO THE CONTAINER FOR EXAMINATION
# docker run -d --name test nba_layer
# docker exec -it test /bin/sh