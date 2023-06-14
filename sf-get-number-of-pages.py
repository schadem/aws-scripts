import argparse
import boto3
import json


def get_number_of_pages(state_machine_arn):
    # Create a Step Functions client
    client = boto3.client('stepfunctions')
    total_number_of_pages = 0

    next_token = None
    next = True
    while next:
        if next_token:
            response = client.list_executions(
                stateMachineArn=state_machine_arn,
                statusFilter='SUCCEEDED',
                nextToken=next_token
            )  # List all executions for the state machine
        else:
            response = client.list_executions(
                stateMachineArn=state_machine_arn, statusFilter='SUCCEEDED')

        # Retrieve "numberOfPages" output for each execution
        for execution in response['executions']:
            execution_arn = execution['executionArn']
            execution_output = client.get_execution_history(
                executionArn=execution_arn,
                reverseOrder=True,
                includeExecutionData=True)

            # Find the task with name "OpenSearchWorkflow-Decider"
            for event in execution_output['events']:
                # print(event)
                if event['type'] == 'TaskStateExited' \
                and 'stateExitedEventDetails' in event \
                and 'name' in event['stateExitedEventDetails'] \
                and event['stateExitedEventDetails']['name'] == 'OpenSearchWorkflow-Decider':
                    # Retrieve the "numberOfPages" output
                    output = json.loads(
                        event['stateExitedEventDetails']['output'])
                    number_of_pages = output['numberOfPages']
                    print(f"{execution_arn},{number_of_pages}")
                    total_number_of_pages += int(number_of_pages)

        if 'nextToken' in response:
            next_token = response['nextToken']
        else:
            next = False
    return total_number_of_pages


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
    print(get_number_of_pages(args.state_machine_arn))
