"""Lambda handler for forwarding messages from SQS to Kinesis Firehose."""

import boto3
import config
import lambdalogging
import json

LOG = lambdalogging.getLogger(__name__)
FIREHOSE = boto3.client('firehose')


def handler(event, context):
    """Forward SQS messages to Kinesis Firehose Delivery Stream."""
    LOG.info('Received event: %s', event)
    if 'Records' not in event:
        LOG.info('No records in event')
        return

    for record in event['Records']:
        content = json.dumps(record)

        response = FIREHOSE.put_record(
            DeliveryStreamName = config.FIREHOSE_DELIVERY_STREAM_NAME,
            Record = {'Data': content + "\n"}
        )
        LOG.debug('Firehose response: %s', response)
