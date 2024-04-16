#!/bin/bash

# to give permission to the script (run this the first time)
# chmod +x build_lambda.sh
# to run the script
# ./build_lambda.sh

# as per ECR documentation, we need to login first
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 471112589532.dkr.ecr.us-east-1.amazonaws.com

docker build -t nba_navigator -f Dockerfile .

docker tag nba_navigator:latest 471112589532.dkr.ecr.us-east-1.amazonaws.com/nba_navigator:latest

docker push 471112589532.dkr.ecr.us-east-1.amazonaws.com/nba_navigator:latest

# as per Lambda documentation, this is how we update the lambda function
aws lambda update-function-code \
    --function-name NbaNavigator \
    --image-uri 471112589532.dkr.ecr.us-east-1.amazonaws.com/nba_navigator:latest \
    --region us-east-1 \

echo "Lambda function updated"
# TO GO INTO THE CONTAINER FOR EXAMINATION
# docker run -d --name test nba_navigator
# docker exec -it test /bin/sh