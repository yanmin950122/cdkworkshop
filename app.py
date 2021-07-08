#!/usr/bin/env python3

import configparser
import enum
import os

from aws_cdk import core
from aws_cdk.core import Tags
from prod.prod_stack import ProdStack, VPCConfig
from basic.basic_stack import BasicStack


class EnvironmentType(enum.Enum):
    PRODUCT = "PRODUCT"
    TEST = "TEST"
    DEV = "DEV"


class GenerateType(enum.Enum):
    VPC = "VPC"
    BASIC = "BASIC"


def confChosen(generateType: str, environment: str):
    environmentConfig = configparser.ConfigParser()

    if generateType == GenerateType.VPC.value:
        if environment == EnvironmentType.PRODUCT.value:
            environmentConfigPath = "./conf/prod/vpc_prod.ini"
        elif environment == EnvironmentType.TEST.value:
            environmentConfigPath = "./conf/test/vpc_test.ini"
        elif environment == EnvironmentType.DEV.value:
            environmentConfigPath = "./conf/dev/vpc_dev.ini"
        else:
            raise Exception("error environment")
    elif generateType == GenerateType.BASIC.value:
        if environment == EnvironmentType.PRODUCT.value:
            environmentConfigPath = "./conf/prod/basic_prod.ini"
        elif environment == EnvironmentType.TEST.value:
            environmentConfigPath = "./conf/test/basic_test.ini"
        elif environment == EnvironmentType.DEV.value:
            environmentConfigPath = "./conf/dev/basic_dev.ini"
        else:
            raise Exception("error environment")
    else:
        raise Exception("error type")

    environmentConfig.read(environmentConfigPath, encoding="utf-8")
    return environmentConfig


def genVPCStacks(app, account, regions, environments, appylyNums):
    for environment in environments:
        environmentConfig = confChosen(GenerateType.VPC.value, environment)
        stackName = environmentConfig.get("basicConf", "stack_name")
        if appylyNums == 0:
            appylyNums = environmentConfig.getint("basicConf", "apply_nums")

        tagsDicts = dict(map(lambda t: (t[0], t[1]), environmentConfig.items("tags")))

        for i in range(appylyNums):
            if appylyNums > 1:
                currStackName = stackName + "-" + str(i + 1)
            else:
                currStackName = stackName
            stack = ProdStack(app, currStackName, vpcConfig=VPCConfig(environmentConfig),
                                       env=core.Environment(account=account, region=regions))
            tag = Tags.of(stack)
            for k, v in tagsDicts.items():
                tag.add(k, v)
            ProdStack.vpcoutput(stack)


def genBasicStacks(app, account, regions, environments):
    for environment in environments:
        environmentConfig = confChosen(GenerateType.BASIC.value, environment)

        stackName = environmentConfig.get("basicConf", "stack_name")

        tagsDicts = dict(map(lambda t: (t[0], t[1]), environmentConfig.items("tags")))
        bucketsDicts = dict(map(lambda bucket: (bucket[0], bucket[1]), environmentConfig.items("buckets")))

        stack = BasicStack(app, stackName, bucketsDicts=bucketsDicts,
                                 env=core.Environment(account=account, region=regions))
        tag = Tags.of(stack)
        for k, v in tagsDicts.items():
            tag.add(k, v)
        BasicStack.vpcoutput(stack)


if __name__ == '__main__':
    app = core.App()

    basicConfig = configparser.ConfigParser()
    basicConfig.read("./conf/base_conf.ini", encoding="utf-8")

    basicConfig.options("default")

    account = basicConfig.get("default", "account")
    regions = basicConfig.get("default", "region")
    environments = basicConfig.get("default", "environment")

    generateType = basicConfig.get("default", "type")

    if "CDK_CL_REGION" in os.environ:
        regions = os.environ["CDK_CL_REGION"]
    if "CDK_CL_ENVIRONMENT" in os.environ:
        environments = os.environ["CDK_CL_ENVIRONMENT"]
    applyNums = 0
    if "CDK_CL_APPLY_NUMS" in os.environ:
        applyNums = int(os.environ["CDK_CL_APPLY_NUMS"])
    if "CDK_CL_GENERATE_TYPE" in os.environ:
        generateType = os.environ["CDK_CL_GENERATE_TYPE"]

    if isinstance(environments, str):
        environments = list(filter(lambda x: x, environments.split("*")))
    # if isinstance(regions, str):
    #     regions = list(filter(lambda x: x, regions.split("*")))

    if generateType == GenerateType.VPC.value:
        genVPCStacks(app, account=account, regions=regions, environments=environments, appylyNums=applyNums)
    elif generateType == GenerateType.BASIC.value:
        genBasicStacks(app, account=account, regions=regions, environments=environments)
    else:
        raise Exception("error type")

    app.synth()
