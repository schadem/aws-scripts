import boto3
import argparse
from tqdm import tqdm


def delete_all_items(table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)  #type: ignore

    response = table.scan()
    items = response.get('Items', [])

    while 'LastEvaluatedKey' in response:
        last_key = response['LastEvaluatedKey']
        response = table.scan(ExclusiveStartKey=last_key)
        items.extend(response.get('Items', []))

    with table.batch_writer() as batch:

        for item in tqdm(items):
            batch.delete_item({'dp': item['dp'], 'ddi': item['ddi']})

    print(f"All items have been deleted from the table '{table_name}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Delete all items from a DynamoDB table.")
    parser.add_argument("--table-name", help="Name of the DynamoDB table")
    args = parser.parse_args()

    table_name = args.table_name
    delete_all_items(table_name)
