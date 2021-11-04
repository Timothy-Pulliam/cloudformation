# Cloudformation Templates

Test with Taskcat

`tascat test run`

Create the Stack

`aws cloudformation create-stack --region ${REGION} --stack-name ${STACK_NAME} \
--template-body file://ecs_app.yaml \
--parameters \
ParameterKey=ApplicationName,ParameterValue=${APP_NAME} \`

Delete the Stack

`aws cloudformation delete-stack --region ${REGION} --stack-name ${STACK_NAME}`
