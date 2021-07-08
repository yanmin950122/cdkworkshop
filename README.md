# VPC&Basic 自助配置化脚本

> 支持conf + cdk 原生指令（默认） / windows psh 批处理脚本两种方式

## 1. windows 批处理启动（适用单region多test环境/多region单cloudformation）
默认配置为conf，使用批处理下会**覆盖**conf配置

**同个堆栈下请保证build/synth/deploy命令行相关参数完全一致** 

### 1.1 cdk-build-to.bat：列举当前应用下堆栈list
        使用方法：cdk-build-to.bat [type] [environment] [region] [apply_nums]
        [type]:堆栈类型 可选值【VPC/BASIC】
        [environment]:堆栈适用环境类型 可选值【PRODUCT/TEST/DEV】
        [region]:部署区域，当前只能指定单个，多个请使用批处理：参考cdk-deploy-multiRegion-to.bat
        [apply_nums]:当前region下部署堆栈数目，一般在test环境使用。
        
        使用示例：cdk-build-to.bat VPC TEST ap-southeast-2 2
        业务含义：列举 使用VPC配置模板在 ``悉尼（ap-southeast-2）`` 下配置两套TEST环境的堆栈信息
        
### 1.2 cdk-synth-to.bat：生成CloudFormation模板并打印到console
        使用方法：cdk-build-to.bat [stack_name] [type] [environment] [region] [apply_nums]
        [stack_name]:堆栈名称 为cdk-build-to.bat输出的堆栈名称
        [type]:堆栈类型 可选值【VPC/BASIC】
        [environment]:堆栈适用环境类型 可选值【PRODUCT/TEST/DEV】
        [region]:部署区域，当前只能指定单个，多个请使用批处理：参考cdk-deploy-multiRegion-to.bat
        [apply_nums]:当前region下部署堆栈数目，一般在test环境使用。

        使用示例：cdk-synth-to.bat IbuTestNetworkAwsStack VPC TEST ap-southeast-2 1
        业务含义：生成IbuTestNetworkAwsStack堆栈对应的CloudFormation模板并在控制台打印

### 1.3 cdk-deploy-to.bat：生成CloudFormation模板并部署到远端
        使用方法：cdk-deploy-to.bat [stack_name] [type] [environment] [region] [apply_nums]
        [stack_name]:堆栈名称 为cdk-build-to.bat列举的堆栈名称；如需部署所有堆栈，请用`--all` 指令
        [type]:堆栈类型 可选值【VPC/BASIC】
        [environment]:堆栈适用环境类型 可选值【PRODUCT/TEST/DEV】
        [region]:部署区域，当前只能指定单个，多个请使用批处理：参考cdk-deploy-multiRegion-to.bat
        [apply_nums]:当前region下部署堆栈数目，一般在test环境使用。

        使用示例：cdk-deploy-to.bat --all VPC TEST ap-southeast-2 2
        业务含义：生成IbuTestNetworkAwsStack-1/-2堆栈对应的CloudFormation模板并部署到ap-southeast-2 区域下
    
### 1.4 cdk-destroy-to.bat：销毁CloudFormation模板并释放远端资源
        使用方法：cdk-destroy-to.bat [stack_name] [type] [environment] [region] [apply_nums]
        [stack_name]:堆栈名称 为cdk-build-to.bat列举的堆栈名称；如需销毁所有堆栈，请用`--all` 指令
        [type]:堆栈类型 可选值【VPC/BASIC】
        [environment]:堆栈适用环境类型 可选值【PRODUCT/TEST/DEV】
        [region]:区域，当前只能指定单个
        [apply_nums]:当前region下堆栈数目，一般在test环境使用。

        使用示例：cdk-destroy-to.bat --all VPC TEST ap-southeast-2 2
        业务含义：销毁ap-southeast-2 区域下 IbuTestNetworkAwsStack-1/-2 CloudFormation模板对应资源
    
### 1.5 cdk-deploy-multiRegion-to.bat：deploy批处理脚本，适用于单模板多region部署

## 2. conf + cdk 原生指令
    修改conf文件。
    相关操作参考cdk 原生指令：
```buildoutcfg
    cdk ls
    cdk synth
    cdk deploy
    cdk destroy
```
