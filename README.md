# Helper Functions for ML Operations
The `RepoManager` class is a utility class designed to manage Git/DagsHub repositories and DVC (Data Version Control) projects. It provides methods to set Git configuration, clone repositories, initialize DVC, add data to DVC, and commit and push changes to the repository. It also provides a method to automate the entire process of initializing a repository with DVC, adding data, and pushing changes.
Please be advised that the functions presented herein are tailored to suit my personal preferences and are not intended for widespread adoption. However, should any individuals find utility in their application, they are welcome to utilize them accordingly.

## Attributes
- `user_name (str)`: The username for the Git/DagsHub accounts.
- `email (str)`: The email for the Git/DagsHub account.
- `token (str)`: The token for the Git/DagsHub accounts.
## Methods
### `run_command(command: str)`
This method runs a shell command and returns its output. It's a general-purpose method that can be used to run any command-line instruction from within the Python environment.

### `set_git_config()`
This method sets the global Git configuration. It uses the user_name, email, and token attributes to set the corresponding Git configuration values.

### `clone_repo(repo: str)`
This method clones a repository to the local runtime. The repo parameter should be a string containing the URL of the repository to clone.

### `initialize_dvc(repo: str)`
This method initializes DVC and sets up remote storage. The repo parameter should be a string containing the URL of the repository to initialize.

### `commit_and_push_changes(repo: str, message: str)`
This method adds all changes to Git, commits them, and pushes to the initialized repository. The repo parameter should be a string containing the URL of the repository to commit and push changes to. The message parameter should be a string containing the commit message.

### `add_data_to_dvc(data_path: str, output_path: str)`
This method adds a directory to DVC and pushes the changes. The data_path parameter should be a string containing the path to the directory to add to DVC. The output_path parameter should be a string containing the path where the DVC files should be stored.

## Installation
You can install this package using pip:
```bash
pip install git+https://github.com/tushar-mahalya/MLOps_Utils.git
```
## Usage
```python
# Import the RepoManager class from the MLOps_utils.helper_functions module
from MLOps_Utils.helper_functions import DVCManager

# Initialize DagsHub Credentials
USER_NAME = # DagsHub UserName
EMAIL = # DagsHub Registered Email
TOKEN = # DagsHub Personal Access Tokens

# Initialize the RepoManager with your DagsHub credentials
manager = RepoManager(USER_NAME, EMAIL, TOKEN)

# Initialze Remote Repository and data path(s)
REPO = # Remote DagsHub Repositry Name
DATA_PATH = # Path of Data Directory (to push)
OUTPUT_PATH = # Path of Directory to save pushed data into

# Initialize the repository with DVC, add the data using DVC, and push the changes to remote
manager.initialize_repo_with_dvc(REPO, DATA_PATH, OUTPUT_PATH)
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the terms of the MIT license.
