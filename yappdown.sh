echo "Starting YappDown"

# Build the Docker image
if docker build -t yappdown . --network=host; then
    echo "Docker image built successfully."
else
    echo "Failed to build Docker image."
    exit 1
fi

# Check if the container exists and remove it if it does
if [ "$(docker ps -aq -f name=yappdown-container)" ]; then
    echo "Removing existing yappdown-container..."
    if docker stop yappdown-container && docker rm -f yappdown-container; then
        echo "Existing container removed successfully."
    else
        echo "Failed to remove existing container."
        exit 1
    fi
fi

# Run the Docker container
if docker run -d -p 8000:8000 --name yappdown-container yappdown; then
    echo "Docker container started successfully."
    echo "YappDown running on: http://localhost:8000"
else
    echo "Failed to start Docker container."
    exit 1
fi