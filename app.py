from crypt import methods
import os
import boto3
from chalice import Chalice, AuthResponse
from chalicelib import auth, db, scrape_jobs, save_data_os


app = Chalice(app_name='job-scrape-api')
app.debug = True
_DB = None
_USER_DB = None

@app.route('/')
def index():
    return {'hello' : 'world'}

# @app.route('/scrape-jobs', api_key_required=False)
# def scrape_jobs_api():
#     result_df = scrape_jobs()
#     # Convert the DataFrame to JSON and return the result
#     #result_dataframe = result_df.to_json(orient='records')
#     return {'result': result_df}

#@app.route('/save-os', api_key_required=False)
@app.schedule('cron(45 10 ? * * *)')
def save_jobs():
    result_df = scrape_jobs()
    os_data = save_data_os(result_df)
    # Convert the DataFrame to JSON and return the result
    #result_dataframe = result_df.to_json(orient='records')
    return {'result': os_data}


# @app.schedule(Cron(0, 0, '*', '*', '?', '*'))
# def my_schedule():
#     return {'hello': 'world'}


# @app.route('/login', methods=['POST'])
# def login():
#     body = app.current_request.json_body
#     record = get_users_db().get_item(
#         Key={'username': body['username']})['Item']
#     jwt_token = auth.get_jwt_token(
#         body['username'], body['password'], record)
#     return {'token': jwt_token}


# @app.authorizer()
# def jwt_auth(auth_request):
#     token = auth_request.token
#     decoded = auth.decode_jwt_token(token)
#     return AuthResponse(routes=['*'], principal_id=decoded['sub'])


# def get_users_db():
#     global _USER_DB
#     if _USER_DB is None:
#         _USER_DB = boto3.resource('dynamodb').Table(
#             os.environ['USERS_TABLE_NAME'])
#     return _USER_DB


# # Rest API code
# def get_app_db():
#     global _DB
#     if _DB is None:
#         _DB = db.DynamoDBTodo(
#             boto3.resource('dynamodb').Table(
#                 os.environ['APP_TABLE_NAME'])
#         )
#     return _DB


# def get_authorized_username(current_request):
#     return current_request.context['authorizer']['principalId']


# @app.route('/todos', methods=['GET'], authorizer=jwt_auth)
# def get_todos():
#     username = get_authorized_username(app.current_request)
#     return get_app_db().list_items(username=username)


# @app.route('/todos', methods=['POST'], authorizer=jwt_auth)
# def add_new_todo():
#     body = app.current_request.json_body
#     username = get_authorized_username(app.current_request)
#     return get_app_db().add_item(
#         username=username,
#         description=body['description'],
#         metadata=body.get('metadata'),
#     )


# @app.route('/todos/{uid}', methods=['GET'], authorizer=jwt_auth)
# def get_todo(uid):
#     username = get_authorized_username(app.current_request)
#     return get_app_db().get_item(uid, username=username)


# @app.route('/todos/{uid}', methods=['DELETE'], authorizer=jwt_auth)
# def delete_todo(uid):
#     username = get_authorized_username(app.current_request)
#     return get_app_db().delete_item(uid, username=username)


# @app.route('/todos/{uid}', methods=['PUT'], authorizer=jwt_auth)
# def update_todo(uid):
#     body = app.current_request.json_body
#     username = get_authorized_username(app.current_request)
#     get_app_db().update_item(
#         uid,
#         description=body.get('description'),
#         state=body.get('state'),
#         metadata=body.get('metadata'),
#         username=username)

