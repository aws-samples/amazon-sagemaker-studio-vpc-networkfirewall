import json
import sagemakerdomain
import userprofile

# Data setup
DomainName = "sagemaker-demo-domain-us-west-2"
UserProfileName = "demouser-profile-us-west-2"
VpcId = "vpc-0c25c864656aabc20"
SageMakerStudioSubnetIds = "subnet-08e7d40bfef63e5ea"
SageMakerSecurityGroupIds = "sg-04cf8c6953e01b74c"
SageMakerExecutionRoleArn = "arn:aws:iam::ACCOUNT_ID:role/sagemaker-studio-vpc-us-west-2-notebook-role"

UserProfileName = "demouser-profile-us-west-2"

DefaultUserSettings = {
    "SecurityGroups":SageMakerSecurityGroupIds.split(","),
    "ExecutionRole":SageMakerExecutionRoleArn
}

UserSettings = {
    "ExecutionRole":SageMakerExecutionRoleArn
}

event = {
    "RequestType":"",
    "PhysicalResourceId":"",
    "ResourceProperties":{}
}

context = None

# Test driver
def test_function(test_name, f, event, context):
    print(f"Testing {test_name}\n****START****")
    print(f"Event:{event['RequestType']}")
    print(f"PhysicalResourceId:{json.dumps(event['PhysicalResourceId'], indent=2)}")
    print(f"ResourceProperties:{json.dumps(event['ResourceProperties'], indent=2)}")

    f(event, context)
    print(f"Testing {f.__name__}****END****")

############################################
# Test
############################################

DomainId = "d-y08vngljr5ez"
# sagemakerdomain, userprofile
test = "sagemakerdomain"
# Create, Update, Delete
event["RequestType"] = "Delete"

if test == "sagemakerdomain":

    # SageMakerDomain test
    event["ResourceProperties"] = {
        "DomainName":DomainName,
        "VpcId":VpcId,
        "SageMakerStudioSubnetIds":SageMakerStudioSubnetIds,
        "DefaultUserSettings":DefaultUserSettings
    }

    if event["RequestType"] == "Create":
        event["PhysicalResourceId"] = None
    else:
        event["PhysicalResourceId"] = DomainId

    test_function("SageMakerDomain", sagemakerdomain.handler, event, context)

elif test == "userprofile":

    # UserProfile test
    event["ResourceProperties"] = {
        "DomainId":DomainId,
        "UserProfileName":UserProfileName,
        "UserSettings":UserSettings
    }

    if event["RequestType"] == "Create":
        event["PhysicalResourceId"] = None
    else:
        event["PhysicalResourceId"] = UserProfileName

    test_function("UserProfile", userprofile.handler, event, context)

