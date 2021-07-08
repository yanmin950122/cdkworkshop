@findstr /B /V @ %~dpnx0 > %~dpn0.ps1 && powershell -ExecutionPolicy Bypass %~dpn0.ps1 %*
@exit /B %ERRORLEVEL%
if ($args.length -eq 5) {
    $env:CDK_CL_GENERATE_TYPE = $($args[1])
    $env:CDK_CL_ENVIRONMENT = $($args[2])
    $env:CDK_CL_REGION = $($args[3])
    $env:CDK_CL_APPLY_NUMS = $($args[4])
    npx cdk destroy $($args[0])
    exit $lastExitCode
}
if ($args.length -eq 4) {
    $env:CDK_CL_GENERATE_TYPE = $($args[1])
    $env:CDK_CL_ENVIRONMENT = $($args[2])
    $env:CDK_CL_REGION = $($args[2])
    npx cdk destroy $($args[0])
    exit $lastExitCode
}
if ($args.length -eq 3) {
    $env:CDK_CL_GENERATE_TYPE = $($args[1])
    $env:CDK_CL_ENVIRONMENT = $($args[2])
    npx cdk destroy $($args[0])
    exit $lastExitCode
}
if ($args.length -eq 2) {
    $env:CDK_CL_GENERATE_TYPE = $($args[1])
    npx cdk destroy $($args[0])
    exit $lastExitCode
} else {
    [console]::error.writeline("Provide account and region as first two args.")
    [console]::error.writeline("Additional args are passed through to cdk deploy.")
    exit 1
}