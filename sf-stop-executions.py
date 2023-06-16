import argparse
import boto3


def stop_executions(state_machine_arn):
    # Create a Step Functions client
    client = boto3.client('stepfunctions')

    next_token = None
    next = True
    while next:
        if next_token:
            response = client.list_executions(
                stateMachineArn=state_machine_arn, nextToken=next_token,
                statusFilter='RUNNING'
            )  # List all executions for the state machine
        else:
            response = client.list_executions(
                stateMachineArn=state_machine_arn, statusFilter='RUNNING')

        for execution in response['executions']:
            execution_arn = execution['executionArn']
            client.stop_execution(executionArn=execution_arn)
            print(f"Stopped execution: {execution_arn}")
        # Retrieve "numberOfPages" output for each execution

        if 'nextToken' in response:
            next_token = response['nextToken']
        else:
            next = False

    # Stop each running execution


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Stop running executions in AWS Step Functions')
    parser.add_argument(
        '--state_machine_arn',
        type=str,
        default=
        'arn:aws:states:us-east-1:913165245630:stateMachine:OpenSearchWorkflow14402093-jvlu9HvEnpCf',
        help='ARN of the state machine')
    args = parser.parse_args()

    # Call the function to stop executions
    stop_executions(args.state_machine_arn)
