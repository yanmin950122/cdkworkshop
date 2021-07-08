@echo off
rem cdk-deploy-to-prod.bat
call cdk-deploy-to.bat --all VPC TEST ap-southeast-2 2 %* || exit /B;
call cdk-deploy-to.bat --all VPC TEST ca-central-1 2 %*;