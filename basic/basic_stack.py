from aws_cdk import (
    aws_ec2 as ec2,
    aws_s3 as s3,
    core
)


class BasicStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, bucketsDicts: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.bucketsList = []
        for key, value in bucketsDicts.items():
            bucket = s3.Bucket(self, key, bucket_name=value)
            self.bucketsList.append(bucket)

    def vpcoutput(self):

        vpcOutput = {
            "buckets_lists": self.bucketsList}

        for k, v in vpcOutput.items():
            core.CfnOutput(self, k, value=str(v))
