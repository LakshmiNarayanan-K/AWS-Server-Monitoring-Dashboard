
import boto3
import os
from datetime import datetime, timedelta, timezone

# AWS Configuration
REGION = os.getenv("AWS_REGION", "us-east-1")
INSTANCE_ID = os.getenv("INSTANCE_ID")

# AWS Clients
ec2 = boto3.client("ec2", region_name=REGION)
cloudwatch = boto3.client("cloudwatch", region_name=REGION)


# Get EC2 Server Details
def get_server_details():

    response = ec2.describe_instances(
        InstanceIds=[INSTANCE_ID]
    )

    instance = response["Reservations"][0]["Instances"][0]

    return {
        "id": instance["InstanceId"],
        "state": instance["State"]["Name"],
        "type": instance["InstanceType"],
        "ip": instance.get("PublicIpAddress", "Not Available")
    }


# Get CloudWatch Metrics
def get_metric(metric_name):

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=1)

    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName=metric_name,
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": INSTANCE_ID
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=["Average"]
    )

    datapoints = sorted(
        response["Datapoints"],
        key=lambda x: x["Timestamp"]
    )

    return [
        {
            "time": point["Timestamp"].strftime("%H:%M"),
            "value": round(point["Average"], 2)
        }
        for point in datapoints
    ]


# Get All Monitoring Data
def get_monitoring_data():

    return {
        "cpu": get_metric("CPUUtilization"),

        "network_in": get_metric("NetworkIn"),

        "network_out": get_metric("NetworkOut"),

        "status_check": get_metric("StatusCheckFailed"),

        "system_status": get_metric("StatusCheckFailed_System"),

        "instance_status": get_metric("StatusCheckFailed_Instance")
    }
