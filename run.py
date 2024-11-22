from app import create_app
from app.extensions import socketio
from pyngrok import ngrok  # Use pyngrok instead of a generic ngrok import
import time

# Create the Flask app
app = create_app()

if __name__ == "__main__":


    ngrok.set_auth_token("2pBTiurjJeNA5XPr04weW17H3p0_CMRmX8y4U8pokWK79vfa") 

    listener = ngrok.connect(5000)

    # Output ngrok URL to console
    print(f"Ingress established at {listener}")

    
    # Run the SocketIO server
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)


    # Keep the listener alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Closing listener")
        ngrok.disconnect(listener)  # Disconnect the tunnel when done