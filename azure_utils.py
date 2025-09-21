import subprocess
import json
import time
from logger import logger

def execute_azure_cli(command):
    """
    Executes an Azure CLI command with exponential backoff retry mechanism.

    Args:
        command (list): A list of strings representing the full Azure CLI command.

    Returns:
        dict: The JSON-parsed output of the command, or None if an error occurs.
    """
    retries = 5
    delay = 1
    for i in range(retries):
        try:
            process = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True
            )
            print(json.loads(process.stdout))
            return json.loads(process.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"Command '{' '.join(command)}' failed with error: {e.stderr}")
            if i < retries - 1:
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
            else:
                logger.error("Max retries reached. Command execution failed.")
                return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from command output: {e.stdout}")
            return None

def create_azure_devops_repo(organization, project, repo_name):
    """
    Creates an Azure DevOps repository and returns its unique ID.

    This function calls the 'az repos create' command via the execute_azure_cli
    utility and then parses the resulting dictionary to extract the repository 'id'.

    Args:
        organization (str): The Azure DevOps organization URL.
        project (str): The name of the Azure DevOps project.
        repo_name (str): The name of the new repository.

    Returns:
        str: The unique ID (GUID) of the created repository, or None if an
             error occurs or the ID cannot be found.
    """
    command = [
        "az", "repos", "create",
        "--org", organization,
        "--project", project,
        "--name", repo_name
    ]
    
    # Step 1: Execute the command. `repo_data` will be a dictionary or None.
    repo_data = execute_azure_cli(command)
    
    # Step 2: Check if the command was successful and returned data.
    if repo_data:
        # Step 3: Safely extract the 'id' from the dictionary.
        # The .get() method is safer than direct key access (repo_data['id'])
        # because it returns None if the key is not found, preventing a crash.
        repo_id = repo_data.get('id')
        repo_url = repo_data.get('remoteUrl')
        if repo_id:
            logger.info(f"Successfully retrieved repository ID: {repo_id}")
            return repo_id,repo_url
        else:
            logger.error(f"Repository may have been created, but 'id' key was not found in the response.")
            logger.debug(f"Full response received: {repo_data}")
            return None
    else:
        # If repo_data is None, it means execute_azure_cli failed and already logged the error.
        logger.error(f"Could not create or retrieve data for repository '{repo_name}'.")
        return None



if __name__ == '__main__':
    # Example usage:
    # Replace with your actual organization, project, and repo name
    
    org_url = "http://192.168.10.22:8080/tfs/RPKavoshDevOps/"
    project_name = "SAJAK"
    repository_name = "rpk-app-test"

    print(f"Attempting to create repository '{repository_name}' in project '{project_name}'...")
    result = create_azure_devops_repo(org_url, project_name, repository_name)

    print(result)