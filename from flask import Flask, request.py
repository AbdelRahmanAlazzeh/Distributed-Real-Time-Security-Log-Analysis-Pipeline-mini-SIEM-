from flask import Flask, request
import json

# Initialize the Flask application
app = Flask(__name__)

# This is the "Route". It tells the app: "If someone sends data to /logs, do this..."
@app.route('/logs', methods=['POST'])
def receive_logs():
    try:
        # Fluent Bit sends logs as a JSON list
        logs = request.get_json()
        
        # Loop through each log entry in the batch
        for entry in logs:
            # Depending on configuration, the message might be in 'log' or 'message' key
            # We check both to be safe
            log_message = entry.get('log') or entry.get('message') or str(entry)
            
            print(f"📥 RECEIVED LOG: {log_message}")
            
            # Simple Security Logic: Check for 'Failed password'
            if log_message and "Failed password" in log_message:
                print(f"🚨 ALERT: Brute force attempt detected!")
                print(f"   Details: {log_message}")
                print("-" * 30)
                
        return "OK", 200
        
    except Exception as e:
        print(f"Error processing log: {e}")
        return "Error", 500

# Start the server on 0.0.0.0 to accept external connections (from Kali)
if __name__ == '__main__':
    print("🚀 SIEM App is running on Port 8080...")
    print("Waiting for logs from Kali...")
    app.run(host='0.0.0.0', port=8080)
    