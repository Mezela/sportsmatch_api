from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.MessageModel import MessageModel, MessageSchema

message_api = Blueprint('message_api', __name__)
message_schema = MessageSchema()

def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

@message_api.route('/<int:game_id>', methods=['GET'])
@Auth.auth_required
def get_all_messages(game_id):
    """
    Get all messages for game
    """
    messages = MessageModel.get_all_game_messages(game_id)
    data = message_schema.dump(messages, many=True)
    return custom_response(data, 200)

@message_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Message
    """
    req_data = request.get_json()
    data = message_schema.load(req_data)
    message = MessageModel(data)
    message.save()
    data = message_schema.dump(message)
    return custom_response(data, 201)
