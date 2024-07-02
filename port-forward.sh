#!/bin/bash

# Ensure kubectl is installed and configured
if ! command -v kubectl &> /dev/null; then
    echo "kubectl could not be found"
    exit 1
fi

# Set kubeconfig path if needed
export KUBECONFIG=/path/to/your/kubeconfig

# Function to start port forwarding
start_port_forward() {
    kubectl port-forward svc/flaskmarket-service 3000:80 > port-forward.log 2>&1 &
    echo "Port forwarding started on localhost:8080"
}

# Function to stop port forwarding
stop_port_forward() {
    # Find and kill the kubectl port-forward process
    pkill -f "kubectl port-forward svc/flaskmarket-service"
    echo "Port forwarding stopped"
}

# Check command-line arguments
case "$1" in
    start)
        start_port_forward
        ;;
    stop)
        stop_port_forward
        ;;
    restart)
        stop_port_forward
        start_port_forward
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac

exit 0
