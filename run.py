from app import create_app
from app.extensions import socketio
from pyngrok import ngrok  # Use pyngrok instead of a generic ngrok import
import time

# Create the Flask app
app = create_app()

if __name__ == "__main__":
    # Run the SocketIO server
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

    # Establish ngrok tunnel
    # You can specify your authtoken directly or set it in your environment variables
    ngrok.set_auth_token("YOUR_NGROK_AUTH_TOKEN")  # Replace with your actual token

    # Forward a port (5000) to the public URL
    listener = ngrok.connect(5000)  # Change to 9000 if that's what you want

    # Output ngrok URL to console
    print(f"Ingress established at {listener}")

    # Keep the listener alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Closing listener")
        ngrok.disconnect(listener)  # Disconnect the tunnel when done