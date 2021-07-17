FaceRecognition at the Edge (Raspberry pi)
=====================================

This demo deploy's a face recognition app to an edge device (raspberry pi)
Inference happens at the edge.

Reference: https://github.com/Martlgap/FaceIDLight/

Deploy
-------
1. Create S3 bucket
    `aws s3 create-bucket --bucket facerecognizer-store`
2. Create ECR repository 
    `aws ecr create-repository --repository-name facerecognizer --image-scanning-configuration scanOnPush=true` 
3. Create a Greengrass group
     `aws greengrass create-group --name FaceRecognition`
4. Download Greengrass Core software and certificate key pair
5. Copy above to raspberry pi
6. Install docker engine on core
7. Add user and group for docker
8. Add DockerApplicationDeployment connector to greengrass group
9. Create IAM policy for S3 access from greengrass service role 
   ```
   {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "s3:GetObject*",
                    "s3:GetBucket*",
                    "s3:List*"
                ],
                "Resource": [
                    "arn:aws:s3:::facerecognizer-store",
                    "arn:aws:s3:::facerecognizer-store/*"
                ],
                "Effect": "Allow"
            }
        ]
   }
   ```
10. Create IAM policy for ECR repo access from greengrass service role
   ```
   {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowGetEcrRepositories",
                "Effect": "Allow",
                "Action": [
                    "ecr:GetDownloadUrlForLayer",
                    "ecr:BatchGetImage"
                ],
                "Resource": [
                    "arn:aws:ecr:us-east-2:271900650525:repository/facerecognizer"
                ]
            },
            {
                "Sid": "AllowGetEcrAuthToken",
                "Effect": "Allow",
                "Action": "ecr:GetAuthorizationToken",
                "Resource": "*"
            }
        ]
   }
   ```
11. On raspberry pi execute
    `sudo /greengrass/ggc/core/greenggrassd start`
12. Build, tag and push docker image
    ```
    docker buildx build -t facerecognizer --platform linux/arm/v7 --load .
    docker tag facerecognizer:latest 271900650525.dkr.ecr.us-east-2.amazonaws.com/facerecognizer:latest
    docker push 271900650525.dkr.ecr.us-east-2.amazonaws.com/facerecognizer:latest
    ```
13. Push docker-compose.yaml to S3
    `aws s3 cp docker-compose.yaml s3://facerecognizer-store`
14. Create greengrass deplployment
    `aws greengrass create-deployment --deployment-type NewDeployment --group-id 583403b7-09fa-4496-a29f-94c56dadb12e --group-version-id ba8b947c-205e-416b-bc72-0bf42c0cd8d5`
    
Usage
-----
```
Request:
curl -F image=@larry3.jpeg http://192.168.0.5:5000/recognize

Response:
{
    "elapsed_ms": 899.9291520012775,
    "predictions": [
        {
            "confidence": 39.138180868966245,
            "name": "Larry_Page"
        }
    ]
}
```

