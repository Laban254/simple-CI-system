from flask import Flask, request
import requests
import os
import threading
import time

PORT = 8011
app = Flask(__name__)

# Configuration: Update this with the path to your locally cloned repository
REPO_PATH = "/home/kibe/projects/test_repo"
DISPATCHER_URL = f"http://localhost:{PORT}/dispatch"
REGISTERED_RUNNERS = []
PENDING_COMMITS = []
RUNNER_STATUS = {}
COMMIT_PATH = "/home/kibe/projects/ci/"

# Repository Observer
@app.route('/observe', methods=['GET'])
def observe_repo():
    while True:
        print("Checking for new commits...")
        os.system("./update_repo.sh")
        commit_file_path = os.path.join(COMMIT_PATH, '.commit_id')

        if os.path.exists(commit_file_path):
            with open(commit_file_path, 'r') as f:
                commit_id = f.read().strip()

            if commit_id:
                print(f"Detected new commit {commit_id}")

                # Register a new runner
                runner_id = "runner_" + commit_id
                register_url = f"http://localhost:{PORT}/register"
                response = requests.post(register_url, json={'runner_id': runner_id})
                print(f"Registered new runner {runner_id}, Response: {response.text}")

                # Dispatch the commit
                response = requests.post(DISPATCHER_URL, json={'commit_id': commit_id})
                print(f"Dispatched commit {commit_id}, Response: {response.text}")
        else:
            print(f"No .commit_id file found at {commit_file_path}")

        time.sleep(10)
    return "Observer is running"

# Dispatcher
@app.route('/register', methods=['POST'])
def register_runner():
    runner_id = request.json.get('runner_id')
    if runner_id and runner_id not in REGISTERED_RUNNERS:
        REGISTERED_RUNNERS.append(runner_id)
        print(f"Runner {runner_id} registered.")
    else:
        print(f"Runner {runner_id} already registered or invalid.")
    return "Runner registered"

@app.route('/dispatch', methods=['POST'])
def dispatch_commit():
    commit_id = request.json.get('commit_id')
    if REGISTERED_RUNNERS:
        runner = REGISTERED_RUNNERS.pop(0)
        runner_url = f"http://{runner}:5008/runtest"
        response = requests.post(runner_url, json={'commit_id': commit_id})
        print(f"Dispatched commit {commit_id} to runner {runner}, Response: {response.text}")
    else:
        PENDING_COMMITS.append(commit_id)
    return "Dispatched commit"

@app.route('/results', methods=['POST'])
def handle_results():
    commit_id = request.json.get('commit_id')
    results = request.json.get('results')
    print(f"Results for {commit_id}: {results}")
    return "Results received"

def check_runners():
    while True:
        print("Checking runners...")
        
        # Define a URL for the health check
        health_check_url = "/health"
        
        for runner in REGISTERED_RUNNERS[:]:  # Iterate over a copy of the list
            runner_url = f"http://{runner}:{PORT}{health_check_url}"
            try:
                # Send a health check request
                response = requests.get(runner_url, timeout=5)
                
                if response.status_code == 200:
                    RUNNER_STATUS[runner] = "alive"
                else:
                    print(f"Runner {runner} responded with status code {response.status_code}.")
                    RUNNER_STATUS[runner] = "unresponsive"
                    
            except requests.RequestException as e:
                # Handle the case where the request fails
                print(f"Runner {runner} is unresponsive. Error: {e}")
                RUNNER_STATUS[runner] = "unresponsive"
                
        # Remove unresponsive runners
        for runner, status in list(RUNNER_STATUS.items()):
            if status == "unresponsive":
                if runner in REGISTERED_RUNNERS:
                    REGISTERED_RUNNERS.remove(runner)
                    print(f"Removed unresponsive runner {runner}.")
                
        # Sleep before the next check
        time.sleep(10)

# Test Runner
@app.route('/runtest', methods=['POST'])
def run_tests():
    commit_id = request.json.get('commit_id')
    result = os.system(f"./test_runner_script.sh {commit_id}")
    if result == 0:
        test_results = "All tests passed"
    else:
        test_results = "Tests failed"
    requests.post(DISPATCHER_URL + "/results", json={'commit_id': commit_id, 'results': test_results})
    return "Tests executed"

if __name__ == "__main__":
    # Start dispatcher runner checker in a separate thread
    threading.Thread(target=check_runners).start()

    # Run the Flask app
    app.run(port=PORT)
