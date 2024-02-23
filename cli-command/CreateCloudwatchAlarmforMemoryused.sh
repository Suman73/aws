aws ec2 describe-instances \
    --filters Name=instance-state-name,Values=running \
    --query 'Reservations[*].Instances[*].[InstanceId, Tags[?Key==`Name`].Value | [0], ImageId, InstanceType]' \
    --output table


aws cloudwatch put-metric-alarm --alarm-name testalarm2 --comparison-operator GreaterThanThreshold --evaluation-periods 1 --datapoints-to-alarm 1 --threshold 80 --period 300 --namespace CWAgent --metric-name mem_used_percent --statistic Average --dimensions Name=InstanceId,Value=<> Name=ImageId,Value=<> Name=InstanceType,Value=t2.micro --actions-enabled --alarm-actions "arn:aws:sns:your-region:your-account-id:your-topic-name1" --treat-missing-data missing
