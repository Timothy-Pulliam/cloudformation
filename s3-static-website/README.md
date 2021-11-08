If you are creating and deleting a bucket with the same name over and over, you may run into an issue where your stack gets stuck in CREATE_IN_PROGRESS state. This is because the previous bucket name is still technically in use. You must wait some time before it can be freed up again.

https://github.com/aws-samples/aws-lex-web-ui/issues/90#issuecomment-822393500
