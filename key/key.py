from flask import Flask, render_template, request, redirect, url_for, flash
import secrets
import string
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Webhook URL (replace with your actual webhook URL)
WEBHOOK_URL = 'https://discord.com/api/webhooks/1305429441328971836/jJ3taeVbhDVsBXPS8_6ZqaooaR_ctBhyLi_7m9T7xhc1zELQi0S2mI6jJulQkB_QsslH'

# Store the generated key in memory (in a production environment, consider a more secure storage)
generated_key = None

def generate_key(length=10):
    """
    Generates a secure random key.
    
    Args:
    length (int): Length of the key to generate.
    
    Returns:
    str: A randomly generated key.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def send_to_discord(message):
    """
    Sends a message to Discord via webhook.
    
    Args:
    message (str): The message to send to Discord.
    """
    payload = {
        "content": message
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending to Discord: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    global generated_key
    
    # Generate a new key on page load and send it to Discord webhook
    if generated_key is None:
        generated_key = generate_key()
        send_to_discord(f"Generated Key: {generated_key}")

    if request.method == 'POST':
        # Retrieve the key entered by the user
        user_key = request.form.get('key')

        # Check if the entered key matches the generated key
        if user_key == generated_key:
            flash("Thank you! Key is correct.", "success")
            generated_key = None  # Reset key after successful use
        else:
            flash("Invalid key. Please try again.", "error")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
