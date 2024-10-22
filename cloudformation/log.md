Configuring SAM deploy
======================

        Looking for config file [samconfig.toml] :  Found
        Reading default arguments  :  Success

        Setting default arguments for 'sam deploy'
        =========================================
        Stack Name [thumbnail-fastapi-app]:
        AWS Region [us-east-1]:
        #Shows you resources changes to be deployed and require a 'Y' to initiate deploy
        Confirm changes before deploy [Y/n]:
        #SAM needs permission to be able to create roles to connect to the resources in your template
        Allow SAM CLI IAM role creation [Y/n]:
        #Preserves the state of previously provisioned resources when an operation fails
        Disable rollback [Y/n]:
The resource AWS::Serverless::Function 'FastApiFunction' has specified ECR registry image for ImageUri. It will not be built and SAM CLI does
not support invoking it locally.
        Save arguments to configuration file [Y/n]:
        SAM configuration file [samconfig.toml]:
        SAM configuration environment [default]:

        Looking for resources needed for deployment:

        Managed S3 bucket: aws-sam-cli-managed-default-samclisourcebucket-nncslkmn7fdx
        A different default S3 bucket can be set in samconfig.toml and auto resolution of buckets turned off by setting resolve_s3=False

        Saved arguments to config file
        Running 'sam deploy' for future deployments will use the parameters saved above.
        The above parameters can be changed by modifying samconfig.toml
        Learn more about samconfig.toml syntax at
        https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-config.html


        Deploying with following values
        ===============================
        Stack name                   : thumbnail-fastapi-app
        Region                       : us-east-1
        Confirm changeset            : True
        Disable rollback             : True
        Deployment s3 bucket         : aws-sam-cli-managed-default-samclisourcebucket-nncslkmn7fdx
        Capabilities                 : ["CAPABILITY_IAM"]
        Parameter overrides          : {}
        Signing Profiles             : {}

Initiating deployment
=====================

File with same data already exists at thumbnail-fastapi-app/bbf28313384d0198162e90769ab57609.template, skipping upload


Waiting for changeset to be created..

CloudFormation stack changeset
-----------------------------------------------------------------------------------------------------------------------------------------
Operation                          LogicalResourceId                  ResourceType                       Replacement
-----------------------------------------------------------------------------------------------------------------------------------------
+ Add                              ApiGatewayDeployment29c67dd358     AWS::ApiGateway::Deployment        N/A
+ Add                              ApiGatewayProdStage                AWS::ApiGateway::Stage             N/A
+ Add                              ApiGateway                         AWS::ApiGateway::RestApi           N/A
+ Add                              FastApiFunction                    AWS::Lambda::Function              N/A
+ Add                              LambdaApiGatewayInvoke             AWS::Lambda::Permission            N/A
+ Add                              LambdaExecutionRole                AWS::IAM::Role                     N/A
+ Add                              StoriBucketPolicy                  AWS::S3::BucketPolicy              N/A
+ Add                              StoriBucket                        AWS::S3::Bucket                    N/A
-----------------------------------------------------------------------------------------------------------------------------------------


Changeset created successfully. arn:aws:cloudformation:us-east-1:440744260607:changeSet/samcli-deploy1729615642/3e3185e4-438c-4d20-8414-c290643

49de3


Previewing CloudFormation changeset before deployment
======================================================
Deploy this changeset? [y/N]: y

2024-10-22 10:47:32 - Waiting for stack create/update to complete

CloudFormation events from stack operations (refresh every 5.0 seconds)
-----------------------------------------------------------------------------------------------------------------------------------------
ResourceStatus                     ResourceType                       LogicalResourceId                  ResourceStatusReason
-----------------------------------------------------------------------------------------------------------------------------------------
CREATE_IN_PROGRESS                 AWS::CloudFormation::Stack         thumbnail-fastapi-app              User Initiated
CREATE_IN_PROGRESS                 AWS::S3::Bucket                    StoriBucket                        -
CREATE_IN_PROGRESS                 AWS::S3::Bucket                    StoriBucket                        Resource creation Initiated
CREATE_COMPLETE                    AWS::S3::Bucket                    StoriBucket                        -
CREATE_IN_PROGRESS                 AWS::IAM::Role                     LambdaExecutionRole                -
CREATE_IN_PROGRESS                 AWS::IAM::Role                     LambdaExecutionRole                Resource creation Initiated
CREATE_COMPLETE                    AWS::IAM::Role                     LambdaExecutionRole                -
CREATE_IN_PROGRESS                 AWS::S3::BucketPolicy              StoriBucketPolicy                  -
CREATE_IN_PROGRESS                 AWS::Lambda::Function              FastApiFunction                    -
CREATE_IN_PROGRESS                 AWS::S3::BucketPolicy              StoriBucketPolicy                  Resource creation Initiated
CREATE_IN_PROGRESS                 AWS::Lambda::Function              FastApiFunction                    Resource creation Initiated
CREATE_COMPLETE                    AWS::S3::BucketPolicy              StoriBucketPolicy                  -
CREATE_IN_PROGRESS -               AWS::Lambda::Function              FastApiFunction                    Eventual consistency check
CONFIGURATION_COMPLETE                                                                                   initiated
CREATE_IN_PROGRESS                 AWS::ApiGateway::RestApi           ApiGateway                         -
CREATE_IN_PROGRESS                 AWS::ApiGateway::RestApi           ApiGateway                         Resource creation Initiated
CREATE_COMPLETE                    AWS::ApiGateway::RestApi           ApiGateway                         -
CREATE_IN_PROGRESS                 AWS::Lambda::Permission            LambdaApiGatewayInvoke             -
CREATE_IN_PROGRESS                 AWS::ApiGateway::Deployment        ApiGatewayDeployment29c67dd358     -
CREATE_IN_PROGRESS                 AWS::Lambda::Permission            LambdaApiGatewayInvoke             Resource creation Initiated
CREATE_IN_PROGRESS                 AWS::ApiGateway::Deployment        ApiGatewayDeployment29c67dd358     Resource creation Initiated
CREATE_COMPLETE                    AWS::Lambda::Permission            LambdaApiGatewayInvoke             -
CREATE_COMPLETE                    AWS::ApiGateway::Deployment        ApiGatewayDeployment29c67dd358     -
CREATE_COMPLETE                    AWS::Lambda::Function              FastApiFunction                    -
CREATE_IN_PROGRESS                 AWS::ApiGateway::Stage             ApiGatewayProdStage                -
CREATE_IN_PROGRESS                 AWS::ApiGateway::Stage             ApiGatewayProdStage                Resource creation Initiated
CREATE_COMPLETE                    AWS::ApiGateway::Stage             ApiGatewayProdStage                -
CREATE_COMPLETE                    AWS::CloudFormation::Stack         thumbnail-fastapi-app              -
-----------------------------------------------------------------------------------------------------------------------------------------

CloudFormation outputs from deployed stack
--------------------------------------------------------------------------------------------------------------------------------------------
Outputs
--------------------------------------------------------------------------------------------------------------------------------------------
Key                 ApiEndpoint
Description         API Gateway endpoint URL for Prod stage
Value               https://0mcdd5t4kj.execute-api.us-east-1.amazonaws.com/Prod/

Key                 FastApiFunctionArn
Description         FastAPI Lambda Function ARN
Value               arn:aws:lambda:us-east-1:440744260607:function:FastApiFunction
--------------------------------------------------------------------------------------------------------------------------------------------


Successfully created/updated stack - thumbnail-fastapi-app in us-east-1
