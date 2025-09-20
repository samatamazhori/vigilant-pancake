
import os
import git
from git.exc import GitCommandError

class GitManager:
    """A class to manage Git repositories."""

    def __init__(self, repo_path=None):
        """
        Initializes the GitManager.

        Args:
            repo_path (str, optional): The path to the repository. Defaults to None.
        """
        self.repo = None
        if repo_path:
            try:
                self.repo = git.Repo(repo_path)
            except git.InvalidGitRepositoryError:
                print(f"Error: Not a valid Git repository: {repo_path}")
            except git.NoSuchPathError:
                print(f"Error: Path does not exist: {repo_path}")

    def init_repo(self, path):
        """
        Initializes a new Git repository.

        Args:
            path (str): The path where the repository will be initialized.
        """
        try:
            self.repo = git.Repo.init(path)
            print(f"Initialized empty Git repository in {path}")
        except GitCommandError as e:
            print(f"Error initializing repository: {e}")

    def clone_repo(self, url, destination_path):
        """
        Clones a repository from a URL.

        Args:
            url (str): The URL of the repository to clone.
            destination_path (str): The local path to clone the repository into.
        """
        try:
            self.repo = git.Repo.clone_from(url, destination_path)
            print(f"Cloned repository from {url} to {destination_path}")
        except GitCommandError as e:
            print(f"Error cloning repository: {e}")

    def checkout_branch(self, branch_name):
        """
        Checks out a specified branch.

        Args:
            branch_name (str): The name of the branch to check out.
        """
        if not self.repo:
            print("Error: Repository not initialized.")
            return

        try:
            self.repo.git.checkout(branch_name)
            print(f"Checked out branch: {branch_name}")
        except GitCommandError as e:
            print(f"Error checking out branch: {e}")

    def add_remote(self, name, url):
        """
        Adds a new remote to the repository.

        Args:
            name (str): The name of the remote.
            url (str): The URL of the remote.
        """
        if not self.repo:
            print("Error: Repository not initialized.")
            return

        try:
            self.repo.create_remote(name, url)
            print(f"Added remote '{name}' with URL: {url}")
        except GitCommandError as e:
            print(f"Error adding remote: {e}")

    def add_all(self):
        """Stages all new and modified files."""
        if not self.repo:
            print("Error: Repository not initialized.")
            return

        try:
            self.repo.git.add(A=True)
            print("Staged all new and modified files.")
        except GitCommandError as e:
            print(f"Error staging files: {e}")

    def commit_changes(self, message):
        """
        Creates a new commit with the given message.

        Args:
            message (str): The commit message.
        """
        if not self.repo:
            print("Error: Repository not initialized.")
            return

        try:
            self.repo.index.commit(message)
            print(f"Committed changes with message: '{message}'")
        except GitCommandError as e:
            print(f"Error committing changes: {e}")

    def push_to_remote(self, remote_name, branch_name):
        """
        Pushes commits to a remote branch.

        Args:
            remote_name (str): The name of the remote to push to.
            branch_name (str): The name of the branch to push.
        """
        if not self.repo:
            print("Error: Repository not initialized.")
            return

        try:
            origin = self.repo.remote(name=remote_name)
            origin.push(refspec=f"{branch_name}:{branch_name}")
            print(f"Pushed to {remote_name}/{branch_name}")
        except GitCommandError as e:
            print(f"Error pushing to remote: {e}")

if __name__ == '__main__':
    # Example usage:
    # Note: This example will create a new directory 'test_repo'
    repo_path = "test_repo"
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)

    # Initialize a new repository
    git_manager = GitManager()
    git_manager.init_repo(repo_path)

    # Create a new file and commit it
    with open(os.path.join(repo_path, "README.md"), "w") as f:
        f.write("# Test Repository\n")

    git_manager.add_all()
    git_manager.commit_changes("Initial commit")

    # The following examples require a remote repository
    # git_manager.add_remote("origin", "https://github.com/user/repo.git")
    # git_manager.push_to_remote("origin", "master")
