#!/usr/bin/env python3
import argparse
from datetime import datetime
import json
import boto3
import botocore


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--s3-endpoint",
        help="s3 endpoint",
        default="http://rook-ceph-rgw-ceph-objectstore."
        "rook-ceph.svc.cluster.local:80",
    )
    parser.add_argument(
        "--s3-accesskey", required=True, help="s3 accesskey", default=None
    )
    parser.add_argument(
        "--s3-secretkey", required=True, help="s3 secretkey", default=None
    )
    parser.add_argument(
        "--s3-bucket",
        help="target s3 bucket name",
        default="seongryong-1",
    )
    parser.add_argument(
        "--kafka-username", required=True, help="kafka username", default=None
    )
    parser.add_argument(
        "--kafka-password", required=True, help="kafka password", default=None
    )
    parser.add_argument(
        "--kafka-endpoint",
        help="kafka endpoint",
        default="redpanda.redpanda.svc.cluster.local",
    )
    parser.add_argument("--kafka-port", help="kafka port", default="9093")
    parser.add_argument(
        "--kafka-mechanism",
        help="kafka mechanism",
        default="SCRAM-SHA-512",
    )
    parser.add_argument(
        "--kafka-topic",
        help="kafka topic",
        default=None,
    )
    parser.add_argument("--notification", help="notification name", default=None)
    parser.add_argument("--opaque-data", help="opaque data", default="rsryu")
    parser.add_argument("--loglevel", help="log level [DEBUG/INFO]", default="INFO")

    args = parser.parse_args()

    if args.kafka_topic is None:
        args.kafka_topic = f"notification-{args.s3_bucket}"
    if args.notification is None:
        args.notification = (
            f"notification-{args.s3_bucket}-{datetime.today().strftime('%y%m%d')}"
        )
    if args.loglevel == "DEBUG":
        boto3.set_stream_logger(name="botocore")

    sns = boto3.client(
        "sns",
        endpoint_url=args.s3_endpoint,
        aws_access_key_id=args.s3_accesskey,
        aws_secret_access_key=args.s3_secretkey,
        region_name="ap-northeast-2",
        config=botocore.client.Config(signature_version="s3"),
        use_ssl=False,
        verify=False,
    )
    s3 = boto3.client(
        "s3",
        endpoint_url=args.s3_endpoint,
        aws_access_key_id=args.s3_accesskey,
        aws_secret_access_key=args.s3_secretkey,
        region_name="ap-northeast-2",
        config=botocore.client.Config(signature_version="s3"),
        use_ssl=False,
        verify=False,
    )

    attributes = {}
    attributes["push-endpoint"] = (
        "kafka://"
        f"{args.kafka_username}:{args.kafka_password}@"
        f"{args.kafka_endpoint}:{args.kafka_port}"
    )
    attributes["kafka-ack-level"] = "broker"
    attributes["verify-ssl"] = "false"
    attributes["use-ssl"] = "false"
    attributes["mechanism"] = args.kafka_mechanism
    attributes["OpaqueData"] = args.opaque_data

    BUCKET_NAME = args.s3_bucket
    try:
        s3.head_bucket(Bucket=BUCKET_NAME)
    except botocore.exceptions.ClientError as e:
        print(f"Error: {e}\n" "Bucket does not exist. Please create the bucket first.")
        exit(1)

    TOPIC_NAME = args.kafka_topic
    TOPIC_ARN = sns.create_topic(Name=TOPIC_NAME, Attributes=attributes)["TopicArn"]
    print("Creating Topic...")

    TOPIC_INFO = sns.get_topic_attributes(TopicArn=TOPIC_ARN)
    print(
        "Created kafka topic! \n"
        f"  TOPIC ARN : {TOPIC_ARN}\n"
        f"  TOPIC NAME : {TOPIC_NAME}\n"
        f"  TOPIC INFO : {json.dumps(TOPIC_INFO, indent=4)}\n"
    )

    bucket_notifications_conf = {
        "TopicConfigurations": [
            {
                "Id": args.notification,
                "TopicArn": TOPIC_ARN,
                "Events": ["s3:ObjectCreated:*", "s3:ObjectRemoved:*"],
            }
        ]
    }

    create_bucket_notification = s3.put_bucket_notification_configuration(
        Bucket=BUCKET_NAME, NotificationConfiguration=bucket_notifications_conf
    )

    print("Creating Bucket Notification...")
    check_notification = s3.get_bucket_notification_configuration(Bucket=BUCKET_NAME)
    print(
        "Created Bucket Notification!"
        f"  BUCKET NAME : {BUCKET_NAME}\n"
        f"  NOTIFICATION NAME : {args.notification}\n"
        f"  NOTIFICATION INFO : {json.dumps(check_notification, indent=4)}\n"
    )
