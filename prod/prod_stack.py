from aws_cdk import (
    aws_ec2 as ec2,
    aws_s3 as s3,
    core
)


class VPCConfig:
    def __init__(self, environmentConfig):
        self.vpcName = environmentConfig.get("VPC", "name")
        self.vpcCidr = environmentConfig.get("VPC", "cidr")
        self.vpcMaxAZS = environmentConfig.getint("VPC", "max_azs")
        self.vpcNetGatewaysSize = environmentConfig.getint("VPC", "net_gateways_size")
        self.vpcEndpointName = environmentConfig.get("VPC", "vpc_endpoint_name")

        self.vpcSubnetPublicName = environmentConfig.get("VPC", "subnet_public_name")
        self.vpcSubnetPublicCidrMaskSize = environmentConfig.getint("VPC", "subnet_public_cidr_mask_size")
        self.vpcSubnetPrivateName = environmentConfig.get("VPC", "subnet_private_name")
        self.vpcSubnetPrivateCidrMaskSize = environmentConfig.getint("VPC", "subnet_private_cidr_mask_size")
        self.vpcSubnetIsolatedName = environmentConfig.get("VPC", "subnet_isolated_name")
        self.vpcSubnetIsolatedCidrMaskSize = environmentConfig.getint("VPC", "subnet_isolated_cidr_mask_size")


class ProdStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpcConfig: VPCConfig, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = ec2.Vpc(self, vpcConfig.vpcName,
                           cidr=vpcConfig.vpcCidr,
                           max_azs=vpcConfig.vpcMaxAZS,
                           subnet_configuration=[ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PUBLIC,
                               name=vpcConfig.vpcSubnetPublicName,
                               cidr_mask=vpcConfig.vpcSubnetPublicCidrMaskSize
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.PRIVATE,
                               name=vpcConfig.vpcSubnetPrivateName,
                               cidr_mask=vpcConfig.vpcSubnetPrivateCidrMaskSize
                           ), ec2.SubnetConfiguration(
                               subnet_type=ec2.SubnetType.ISOLATED,
                               name=vpcConfig.vpcSubnetIsolatedName,
                               cidr_mask=vpcConfig.vpcSubnetIsolatedCidrMaskSize
                           )
                           ],
                           # nat_gateway_provider=ec2.NatProvider.gateway(),
                           nat_gateways=vpcConfig.vpcNetGatewaysSize,
                           )
        self.vpcEndpoint = self.vpc.add_s3_endpoint(vpcConfig.vpcEndpointName)  # endpoint

        # self.bucketsList = []
        # for key, value in bucketsDicts.items():
        #     bucket = s3.Bucket(self, key, bucket_name=value)
        #     self.bucketsList.append(bucket)

    def forEachSubNets(self, subnets, subNetType):
        type = "NONE"
        if subNetType == ec2.SubnetType.PUBLIC:
            type = "internet"
        elif subNetType == ec2.SubnetType.PRIVATE:
            type = "application"
        elif subNetType == ec2.SubnetType.ISOLATED:
            type = "protected"
        internetSubnetsInfo = {}
        for i, pubSub in enumerate(subnets):
            subVpcInfo = {"cidr_block": pubSub.ipv4_cidr_block, "vpc_id": pubSub.subnet_id}
            subVpcInfoDic = {type + "_subnet:" + str(i) + "information": subVpcInfo}
            internetSubnetsInfo.update(subVpcInfoDic)
        return internetSubnetsInfo

    def vpcoutput(self):
        vpcOutput = {"vpc_cidr_block": self.vpc.vpc_cidr_block, "vpc_id": self.vpc.vpc_id,
                     "vpc endpoint": self.vpcEndpoint.vpc_endpoint_id}

        subVpcOutput = {
            "internet_subnets": self.forEachSubNets(self.vpc.public_subnets, ec2.SubnetType.PUBLIC),
            "application_subnets": self.forEachSubNets(self.vpc.private_subnets, ec2.SubnetType.PRIVATE),
            "protected_subnets": self.forEachSubNets(self.vpc.isolated_subnets, ec2.SubnetType.ISOLATED)}

        vpcOutput.update(subVpcOutput)

        # bucketOutput = {
        #     "buckets_lists": self.bucketsList}
        #
        # vpcOutput.update(bucketOutput)

        for k, v in vpcOutput.items():
            core.CfnOutput(self, k, value=str(v))
