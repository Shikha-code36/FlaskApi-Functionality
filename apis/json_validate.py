from flask import Flask, request, jsonify, Blueprint
from flask_expects_json import expects_json
import json
from bson import ObjectId, json_util
import mongoservice

jsonValidate = Blueprint("jsonValidate", __name__)


# Define the JSON schema for the list
request_schema = {
    "type": "object",
    "properties": {
        "PositionType": {
            "type": "string",
            "enum": ["PositionType.Buy", "PositionType.Sell"]
        },
        "Lots": {
            "type": "integer",
            "minimum": 1
        },
        "LegStopLoss": {
            "type": "object",
            "properties": {
                "Type": {
                    "type": "string",
                    "enum": [
                        "LegTgtSLType.Percentage",
                        "LegTgtSLType.Points",
                        "LegTgtSLType.UnderlyingPercentage"
                    ]
                },
                "Value": {
                    "type": "integer",
                    "minimum": 0
                }
            },
            "required": ["Type", "Value"]
        },
        "LegTarget": {
            "type": "object",
            "properties": {
                "Type": {
                    "type": "string",
                    "enum": [
                        "LegTgtSLType.Percentage",
                        "LegTgtSLType.Points",
                        "LegTgtSLType.UnderlyingPercentage"
                    ]
                },
                "Value": {
                    "type": "integer",
                    "minimum": 0
                }
            },
            "required": ["Type", "Value"]
        },
        "LegTrailSL": {
            "type": "object",
            "properties": {
                "Type": {
                    "type": "string",
                    "enum": ["None", "TrailStopLossType.Points", "TrailStopLossType.Percentage"]
                },
                "Value": {
                    "type": "object",
                    "properties": {
                        "InstrumentMove": {
                            "type": "integer",
                            "minimum": 0
                        },
                        "StopLossMove": {
                            "type": "integer",
                            "minimum": 0
                        }
                    },
                    "required": ["InstrumentMove", "StopLossMove"]
                }
            },
            "required": ["Type", "Value"]
        },
        "LegMomentum": {
            "type": "object",
            "properties": {
                "Type": {
                    "type": "string",
                    "enum": [
                        "None",
                        "MomentumType.PointsUp",
                        "MomentumType.PointsDown"
                    ]
                },
                "Value": {
                    "type": "integer",
                    "minimum": 0
                }
            },
            "required": ["Type", "Value"]
        },
        "ExpiryKind": {
            "type": "string",
            "enum": ["ExpiryType.Weekly", "ExpiryType.Monthly"]
        },
        "EntryType": {
            "type": "string",
            "enum": ["EntryType.EntryByStrikeType"]
        },
        "StrikeParameter": {
            "type": "string",
            "enum": ["StrikeType.ATM"]
        },
        "InstrumentKind": {
            "type": "string",
            "enum": ["LegType.CE"]
        },
        "LegReentrySL": {
            "type": "object",
            "properties": {
                "Type": {
                    "type": "string",
                    "enum": ["ReentryType.ASAP", "ReentryType.ASAPReverse"]
                },
                "Value": {
                    "type": "integer",
                    "minimum": 0
                }
            },
            "required": ["Type", "Value"]
        },
        "LegReentryTP": {
            "type": "object",
            "properties": {
                "Type": {
                    "type": "string",
                    "enum": ["ReentryType.ASAP", "ReentryType.ASAPReverse"]
                },
                "Value": {
                    "type": "integer",
                    "minimum": 0
                }
            },
            "required": ["Type", "Value"]
        }
    },
    "required": [
        "PositionType",
        "Lots",
        "LegStopLoss",
        "LegTarget",
        "LegTrailSL",
        "LegMomentum",
        "ExpiryKind",
        "EntryType",
        "StrikeParameter",
        "InstrumentKind",
        "LegReentrySL",
        "LegReentryTP"
    ]
}


# Create the authenticate route
@jsonValidate.route('/authenticateJson', methods=['POST'])
@expects_json(request_schema)
def authenticateSchema():
    # Validate the JSON in the request body
    data = request.get_json()

    # Store the list of items in the 'lists' collection in the database
    mongoservice.storelist(data)

    return jsonify({'message': 'List stored successfully'}), 201

# Create the get endpoint to retrieve all lists for the user


@jsonValidate.route('/lists', methods=['GET'])
def get_lists():
    # Retrieve all lists from the 'lists' collection in the database
    lists = mongoservice.findlist()
    # Convert the cursor to a list of documents
    lists = json.loads(json_util.dumps(lists))
    # Return the lists to the client
    return jsonify({'lists': lists})

# Create the get endpoint to retrieve a particular list


@jsonValidate.route('/lists/<list_id>', methods=['GET'])
def get_listbyID(list_id):
    # Convert the list ID to an ObjectId
    list_id = ObjectId(list_id)

    # Retrieve the list with the given ID from the 'lists' collection in the database
    list = mongoservice.findlistbyid(list_id)

    list = json.loads(json_util.dumps(list))

    # Return the list to the client
    return jsonify({'list': list})
