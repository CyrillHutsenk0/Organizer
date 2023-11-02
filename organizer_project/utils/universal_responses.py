from flask import jsonify


def success_response():
    """Success message response"""
    return jsonify({"message": "Success"}), 200
