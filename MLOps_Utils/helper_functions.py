import os
import subprocess
import logging
import mlflow

class RepoManager:
    """
    A class to manage Git repositories and DVC projects.

    This class provides methods to set Git configuration, clone repositories, initialize DVC, 
    add data to DVC, and commit and push changes to the repository. It also provides a method 
    to automate the entire process of initializing a repository with DVC, adding data, and 
    pushing changes.

    Attributes:
        user_name (str): The username for the Git/DagsHub accounts.
        email (str): The email for the Git/DagsHub account.
        token (str): The token for the Git/DagsHub accounts.

    Methods:
        run_command(command: str) -> str: Run a shell command and return its output.
        set_git_config(): Set global Git configuration.
        clone_repo(repo: str): Clone a repository to local runtime.
        initialize_dvc(repo: str): Initialize DVC and set up remote storage.
        commit_and_push_changes(repo: str, message: str): Add all changes to Git, commit them, and push to the initialized repository.
        add_data_to_dvc(data_path: str, output_path: str): Add a directory to DVC and push the DVC-tracked files to the remote storage.
        initialize_repo_with_dvc(repo: str, data_path: str, output_path: str): Initialize a repository with DVC, add data, and push changes.
    """
    
    def __init__(self, user_name: str, email: str, token: str):
        self.user_name = user_name
        self.email = email
        self.token = token
        self.is_git_config = False
        logging.basicConfig(level=logging.INFO)

    def run_command(self, command: str) -> str:
        """
        Run a shell command and return its output.
        """
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        if process.returncode != 0:
            logging.error(f"Error executing command: {command}\nError: {error.decode('utf-8')}")
            return None
        return output.decode('utf-8')

    def set_git_config(self):
        """
        Set global git configuration.
        """
        self.run_command(f'git config --global user.email {self.email}')
        self.run_command(f'git config --global user.name {self.user_name}')
        self.is_git_config = True
        logging.info("Git configuration set.")

    def clone_repo(self, repo: str):
        """
        Clone a repository.
        """
        self.run_command(f'git clone https://{self.user_name}:{self.token}@dagshub.com/{self.user_name}/{repo}.git')
        if not os.path.exists(repo):
            logging.error(f"Error: Failed to clone the repository {repo}")
            return
        os.chdir(repo)
        logging.info(f"Repository {repo} cloned.")

    def initialize_dvc(self, repo: str):
        """
        Initialize DVC and set up remote storage.
        """
        self.run_command('dvc init')
        self.run_command('dvc remote add origin s3://dvc')
        self.run_command(f'dvc remote modify origin endpointurl https://dagshub.com/{self.user_name}/{repo}.s3')
        self.run_command(f'dvc remote modify --local origin access_key_id {self.token}')
        self.run_command(f'dvc remote modify --local origin secret_access_key {self.token}')
        self.run_command('dvc remote default origin')
        logging.info("DVC initialized and remote storage set up.")

    def commit_and_push_changes(self, repo: str, message: str):
        """
        Add all changes to git, commit them, and push to the repository.
        """
        self.run_command('git add .')
        self.run_command(f'git commit -m "{message}"')
        self.run_command(f'git push https://{self.user_name}:{self.token}@dagshub.com/{self.user_name}/{repo}.git')
        logging.info(f"Changes committed and pushed with message: {message}")

    def add_data_to_dvc(self, data_path: str, output_path: str):
        """
        Add a directory to DVC and push the DVC-tracked files to the remote storage.
        """
        self.run_command(f'dvc add {data_path} -o {output_path}')
        self.run_command('dvc push -r origin')
        logging.info(f"Data from {data_path} added to DVC and pushed to remote storage.")

    def initialize_repo_with_dvc(self, repo: str, data_path: str, output_path: str):
        """
        Initialize a repository with DVC, add data, and push changes.
        """
        if not self.is_git_config:
            self.set_git_config()
            print(">>> Git configuration set successfully")

        if not os.path.exists(repo):
            self.clone_repo(repo)
            print(f">>> Repository {repo} cloned successfully")
        else:
            os.chdir(repo)
            print(f">>> Repository {repo} already exists")
    
        if not os.path.exists('.dvc'):
            self.initialize_dvc(repo)
            print(">>> DVC initialized and remote storage set up successfully")
            self.commit_and_push_changes(repo, "Initialize DVC")
            print(">>> Changes committed and pushed to the repository with message: \"Initialize DVC\"")
        else:
            print(">>> DVC already initialized")

        if not os.path.exists(output_path):
            self.add_data_to_dvc(data_path, output_path)
            print(f">>> Data from {data_path} added to DVC and pushed to remote storage")
            self.commit_and_push_changes(repo, "Added Versioned Data")
            print(">>> Changes committed and pushed to the repository with message: \"Added Versioned Data\"")
        else:
            print(f">>> Data from {data_path} already added to Remote with DVC")    
    
    def initialize_tracking(self, repo: str):
        if not self.is_git_config:
            self.set_git_config()
            print(">>> Git configuration set successfully")
        os.environ['MLFLOW_TRACKING_USERNAME'] = self.user_name
        os.environ['MLFLOW_TRACKING_PASSWORD'] = self.token
        MLFLOW_TRACKING_URI = f"https://dagshub.com/{self.user_name}/{repo}.mlflow"
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        print(f'>>> MLFlow Experiment Tracking Initialized\n\tExperiment Tracking URI : {MLFLOW_TRACKING_URI}')

