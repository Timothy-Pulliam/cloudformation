# Deletion Policy Attribute
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html

Retain
CloudFormation keeps the resource without deleting the resource or its contents when its stack is deleted. You can add this deletion policy to any resource type. When CloudFormation completes the stack deletion, the stack will be in Delete_Complete state; however, resources that are retained continue to exist and continue to incur applicable charges until you delete those resources.

# UpdateReplacePolicy attribute
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html

Retain
CloudFormation keeps the resource without deleting the resource or its contents when the resource is replaced. You can add this policy to any resource type. Resources that are retained continue to exist and continue to incur applicable charges until you delete those resources.

If a resource is replaced, the UpdateReplacePolicy retains the old physical resource but removes it from CloudFormation's scope.
