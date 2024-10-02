import sys
sys.path.append("../Webhook")

import json
import traceback
from flask import Flask, request, jsonify
from data.crypto_manager import generate_key, retrieve_encrypted_data, retrieve_salt
from mail.mail_service import send_email, create_welcome_message, extract_email_data
from util.messages_codes import response_success, response_failure, response_not_relevant, response_key_not_found, response_invalid_method

app = Flask(__name__)

# Webhook route
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        try:
            data = request.get_json()

            # Log the received data
            print(f"Received data: {json.dumps(data, indent=4)}")

            # Test connection
            if "test" in data and data["test"] is True:
                recipient_email = "test@domain.com"
                subject = "Webhook Connection Test"
                message = (
                    "Connection test successful.\nWebhook ID: "
                    + data["webhook_id"]
                )

                # Send the test email
                if send_email(recipient_email, subject, message, user, password):
                    return response_success("Connection test completed, email sent!")
                else:
                    return response_failure("Failed to send email.")

            # Verify the presence of 'data' for real events
            if "data" in data:
                # Check for the necessary fields in the payload
                if (
                    data["data"]["action"] == "created"
                    and "performedby_clientname" in data["data"]
                    and data["data"]["performedby_clientname"] == "DesiredClientName"
                ):
                    # Extract the email data using the function from email_service
                    first_name, last_name, full_name, recipient_email, department = extract_email_data(data)

                    subject = "New user created via DesiredClientName"

                    # Create a formatted welcome message using the email_service function
                    message = create_welcome_message(first_name, last_name, full_name, recipient_email, department)

                    if send_email(recipient_email, subject, message, user, password):
                        return response_success("Webhook processed, email sent!")
                    else:
                        return response_failure("Failed to send email.")
                else:
                    # If the event wasn't from DesiredClientName, return status 200 for non-relevant event
                    return response_not_relevant()
            else:
                # If 'data' is not present, return 'data not found in payload'
                return response_key_not_found()

        except Exception as e:
            print(f"\nError processing webhook: {e}")
            traceback.print_exc()
            return response_failure("Error processing webhook")
    else:
        return response_invalid_method()

# Function to initialize the app and request the password
def main():
    # Request the user to input their password to derive the key
    user_password = input("\nEnter your password/key to decrypt the data: ")

    # Retrieve the salt from the environment variables
    salt = retrieve_salt()

    # Generate the key from the password and the salt
    key = generate_key(user_password, salt)

    # Retrieve the encrypted data from the environment variables
    global user, password
    user, password = retrieve_encrypted_data(key)

    # Start the Flask server
    app.run(port=5000)

if __name__ == "__main__":
    main()