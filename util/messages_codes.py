from flask import jsonify

# Function for a successful response (200)
def response_success(message):
    print(f"--> Operation completed: {message}")
    return jsonify({
        "status": "success",
        "message": message
    }), 200

# Function for a failure response (500)
def response_failure(message):
    print(f"--> Operation failed: {message}")
    return jsonify({
        "status": "failure",
        "message": message
    }), 500

# Function for non-relevant event response (200)
def response_not_relevant():
    print("--> Operation ignored: Non-relevant event")
    return jsonify({
        "status": "ignored",
        "message": "Non-relevant event"
    }), 200

# Function for missing data key response (400)
def response_key_not_found():
    print("--> Operation failed: 'data' key not found in payload")
    return jsonify({
        "status": "failure",
        "message": "'data' key not found in payload"
    }), 400

# Function for invalid method response (405)
def response_invalid_method():
    print("--> Operation failed: Invalid method")
    return jsonify({
        "status": "failure",
        "message": "Invalid method"
    }), 405