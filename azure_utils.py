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
    Creates an Azure DevOps repository using the 'az repos create' command.

    Args:
        organization (str): The Azure DevOps organization URL.
        project (str): The name of the Azure DevOps project.
        repo_name (str): The name of the new repository.

    Returns:
        dict: The JSON-parsed output of the command, or None if an error occurs.
    """
    command = [
        "az", "repos", "create",
        "--org", organization,
        "--project", project,
        "--name", repo_name
    ]
    return execute_azure_cli(command)

if __name__ == '__main__':
    # Example usage:
    # Replace with your actual organization, project, and repo name
    org_url = "https://dev.azure.com/your_organization"
    project_name = "your_project"
    repository_name = "new-repo-from-script"

    print(f"Attempting to create repository '{repository_name}' in project '{project_name}'...")
    result = create_azure_devops_repo(org_url, project_name, repository_name)

    if result:
        print("Repository created successfully!")
        print(json.dumps(result, indent=4))
    else:
        print("Failed to create repository.")