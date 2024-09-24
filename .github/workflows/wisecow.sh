#!/usr/bin/env bash

# Define the service port and response file
SRVPORT=4499
RSPFILE=response

# Clean up old response file and create a new named pipe (FIFO)
rm -f $RSPFILE
mkfifo $RSPFILE

# Function to capture API requests
get_api() {
    # Read the incoming request from the client
    read line
    echo $line
}

# Function to handle incoming HTTP requests
handleRequest() {
    get_api
    mod=$(fortune)

    # Prepare the HTTP response with fortune and cowsay
    cat <<EOF > $RSPFILE
HTTP/1.1 200 OK

<pre>$(cowsay "$mod")</pre>
EOF
}

# Check if required commands are installed
prerequisites() {
    echo "Checking for necessary commands..."
    command -v cowsay >/dev/null 2>&1 || { echo "cowsay is not installed. Exiting."; exit 1; }
    command -v fortune >/dev/null 2>&1 || { echo "fortune is not installed. Exiting."; exit 1; }
    command -v nc >/dev/null 2>&1 || { echo "netcat (nc) is not installed. Exiting."; exit 1; }
    echo "All prerequisites met."
}

# Main function to start the server
main() {
    prerequisites
    echo "Wisdom being served on port $SRVPORT..."

    # Run the server loop, listening for connections
    while true; do
        cat $RSPFILE | nc -lN 0.0.0.0 $SRVPORT | handleRequest
        sleep 0.01
    done
}

# Start the main function
main
