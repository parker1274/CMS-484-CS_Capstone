# README

## Bash Script Permissions

If you haven't given the deploy scripts, permissions, run these commands:

``` bash
chmod +x build_lambda.sh
chmod +x build_layer.sh
```

## Layer updates

If you make updates to packages in the lambda, you must update the layer. This does not have to be done every time.

``` bash
./build_layer.sh
```

**Note:** this will re-deploy the Lambda code as well

## Lambda updates

To upload any changes to the Lambda function, use this command:

``` bash
./build_lambda.sh
```

## Testing the Lambda Function

To test the Lambda function, run the command below:

``` bash
curl https://qr7cldaha9.execute-api.us-east-1.amazonaws.com \
    -H "Content-Type: application/json" \
    -d '{"action": "1","model_type": "classifier","TeamA_abbreviation": "BOS","TeamB_abbreviation": "NYK","season": "2023-24","number _seasons": "3","number_past_games": "15"}'
```

Expected output:

``` json
{"prediction_outcome": "Win", "prediction_probability": "100.00%", "probabilities": {"win_probability": "100.00000000%", "loss_probability": "0.00000000%"}}
```

### References

https://docs.aws.amazon.com/lambda/latest/dg/lambda-foundation.html

https://docs.aws.amazon.com/lambda/latest/dg/python-image.html

https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html

https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html

https://github.com/github/gitignore/blob/main/Python.gitignore

https://github.com/GoogleCloudPlatform/getting-started-python/blob/main/optional-kubernetes-engine/.dockerignore
