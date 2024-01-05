from update import update_users_timeline_data
import json


def lambda_handler(event, context):

    update_users_timeline_data()

    return {
        'statusCode': 200,
        'body': json.dumps("Updated listening data in MongoDB")
    }


update_users_timeline_data()
