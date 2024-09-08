# Simple CI System

## Overview

 **Simple CI System** is a basic Continuous Integration (CI) tool designed to automate the process of detecting code changes, running tests, and managing test runners. 

## Features

-   **Commit Detection**: Monitors a Git repository for new commits and updates a tracking file when changes are detected.
-   **Runner Registration**: Allows test runners to register themselves with the CI system, enabling them to receive and execute test jobs.
-   **Commit Dispatching**: Distributes new commits to available registered test runners for execution.
-   **Test Execution**: Executes tests based on the new commits and reports the results back to the CI system.

## Components

1.  **Observer**: Continuously monitors the Git repository for new commits and updates the commit ID file.
2.  **Dispatcher**: Manages the registration of test runners and dispatches new commits to them for testing.
3.  **Runner**: Executes tests on the code for the specified commit and sends the results back to the CI system.
4.  **Health Check**: Periodically checks the status of registered runners to ensure they are responsive.

## How It Works

1.  **Commit Detection**:
    
    -   The system uses a script to check for new commits in the repository.
    -   When a new commit is detected, the system updates a `.commit_id` file.
2.  **Runner Registration**:
    
    -   Test runners can register themselves with the CI system by sending a POST request to the `/register` endpoint.
    -   Registered runners are tracked and can receive test jobs.
3.  **Commit Dispatching**:
    
    -   Upon detecting a new commit, the CI system dispatches the commit to a registered runner by sending a POST request to the runner's `/runtest` endpoint.
4.  **Test Execution**:
    
    -   The test runner executes the tests for the specified commit and sends the results back to the CI system via the `/results` endpoint.
5.  **Health Check**:
    
    -   The system periodically checks the health of registered runners to ensure they are operational.
    -   Unresponsive runners are removed from the list of registered runners.

## Setup

1.  **Clone the Repository**:

    
    `git clone https://github.com/laban254/simple-ci-system.git
    cd simple-ci-system` 
    
2.  **Install Dependencies**: Ensure you have Python and the necessary libraries installed.
    
3.  **Run the CI System**:
    

    
    `python main.py` 
    
4.  **Run the Test Runner**: Ensure that the test runner script is properly configured and executable.
    

## Directory Structure

-   `main.py`: The main script that runs the CI system.
-   `test_runner_script.sh`: A script executed by the test runner to run tests.
-   `update_repo.sh`: A script that updates the local repository and checks for new commits.

