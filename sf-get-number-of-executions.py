import argparse
import boto3


def get_number_of_pages(state_machine_arn):
    # Create a Step Functions client
    client = boto3.client('stepfunctions', region_name='us-east-2')
    total_number_of_executions = 0

    next_token = None
    next = True
    while next:
        if next_token:
            response = client.list_executions(
                stateMachineArn=state_machine_arn, nextToken=next_token
            )  # List all executions for the state machine
        else:
            response = client.list_executions(
                stateMachineArn=state_machine_arn)

        # Retrieve "numberOfPages" output for each execution
        total_number_of_executions += len(response['executions'])

        if 'nextToken' in response:
            next_token = response['nextToken']
        else:
            next = False
    return total_number_of_executions


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Stop running executions in AWS Step Functions')
    parser.add_argument(
        '--state_machine_arn',
        type=str,
        default=
        'arn:aws:states:us-east-2:913165245630:stateMachine:OpenSearchWorkflow14402093-ghbqWqN143Md',
        help='ARN of the state machine')
    args = parser.parse_args()

    # Call the function to stop executions
    print(get_number_of_pages(args.state_machine_arn))
