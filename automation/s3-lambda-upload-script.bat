#c:\opt\rk-dev-env-setup.bat

#zip lambda.zip lambda/main.js
cd lambda
jar -cfM ../lambda.zip main.js
cd ..


aws s3api create-bucket --bucket=rk-terraform-lambda --region=us-east-1

aws s3 cp lambda.zip s3://rk-terraform-lambda/v1.0.0/lambda.zip

aws s3 ls s3://rk-terraform-lambda/v1.0.0/

terraform apply
