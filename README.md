---

# Webhook Email Service

This project demonstrates a webhook integration that processes user creation events and sends an email notification when a new user is created via a client system. It includes encryption for sensitive information such as email credentials, ensuring secure communication with an SMTP server.

## Project Overview

The project is built using:
- **Flask**: To create a simple webhook receiver.
- **SMTP**: To send emails based on the webhook events.
- **Cryptography**: To encrypt and decrypt sensitive data (email credentials) with secure handling.
- **Ngrok**: Used to expose the local server for testing the webhook integration with an external platform.

### Features:
- Handles user creation events triggered by an external client system.
- Encrypts and stores email credentials using a user-provided password.
- Sends email notifications to users when new accounts are created.
- Allows for secure storage of salts and environment variables.
- Well-structured with separation of concerns (encryption, email service, webhook handling).

## Project Structure

```bash
.
├── data
│   ├── crypto_env.py          # Encrypts credentials and stores them in environment variables.
│   ├── crypto_manager.py      # Decrypts credentials and retrieves stored data.
├── mail
│   ├── email_service.py       # Contains logic to send emails and create email messages.
├── util
│   ├── messages_codes.py      # Abstracts response messages and status codes.
├── main
│   ├── webhook_app.py         # Main Flask app to handle webhook requests.
├── README.md                  # Project documentation (this file).
```

### Key Files:

- **crypto_env.py**: Encrypts user credentials and stores them securely using Windows environment variables. **Must be run before starting the webhook service**.
- **crypto_manager.py**: Decrypts the stored credentials at runtime to use for sending emails.
- **email_service.py**: Handles the email sending logic, including building personalized welcome messages.
- **messages_codes.py**: Defines and abstracts HTTP status responses used in the application.
- **webhook_app.py**: The main Flask app that processes webhook events and sends emails when appropriate.

## Prerequisites

Ensure you have the following tools installed on your machine:

- **Python 3.10+**
- **Pip** (Python package manager)
- **Ngrok** (for exposing local development server to the internet)

Install the necessary Python packages by running:

```bash
pip install -r requirements.txt
```

### Packages required:
- `Flask`
- `cryptography`


## Setting Up Ngrok

In this scenario I used Ngrok to expose my local Flask server to the internet for testing with external webhook systems:

1. Download and install [Ngrok](https://ngrok.com/).
2. Run the following command to expose the local Flask app running on port 5000:

```bash
ngrok http 5000
```

This will provide you with a public URL to use for testing webhook events.

## Usage

### Step 1: Encrypt and Store Email Credentials

**Before running the webhook app,** you need to use the `crypto_env.py` script to encrypt your email credentials and store them securely.

1. Run the following command:

```bash
python data/crypto_env.py
```

2. You will be prompted to enter:
   - Your encryption password (used to encrypt and decrypt your credentials).
   - Your email username and password (which will be encrypted and stored in environment variables).

### Step 2: Run the Flask Webhook App

After credentials have been securely stored, you can start the webhook app:

```bash
python main/webhook_app.py
```

This will start the Flask server, listening for POST requests on the `/webhook` route.

### Step 3: Handling Webhook Events

- **Test connection**: The webhook service can send test events to verify the connection.
- **User creation**: When a user is created by the client system, the app sends a welcome email to the user.

### Step 4: Webhook Configuration

In your external client system:
- Set up the webhook URL to point to your Ngrok public URL followed by `/webhook`.
- Ensure your events (e.g., user creation) are configured to trigger the webhook.

## Error Handling

The app includes error handling for:
- Invalid encryption keys.
- Missing environment variables (credentials).
- Invalid or irrelevant webhook events.
- Incorrect passwords during decryption (with multiple retry attempts).

## Contributing

Feel free to fork this project and submit pull requests for improvements or new features. Please ensure your code is clean and follows the existing code style.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---