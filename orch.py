from git_utils import GitManager
from file_utils import remove_files_by_extension, \
    rename_files_and_dirs, replace_content_in_files, \
    remove_file_by_name
from azure_utils import create_azure_devops_repo

def get_dot_net_template():
    TEMPLATE_URL = "ssh://azurenew.rpk.ir:22/tfs/RPKavoshDevOps/SAJAK/_git/rpk-saja-template-dotnet"
    GIT_DIR = "test_repo"
    git = GitManager(GIT_DIR)
    git.clone_repo(TEMPLATE_URL,GIT_DIR)
    git.checkout_branch("develop")
    print("Template is downloaded successfully.")


def clean_dot_net_template():
    TEMPLATE_DIR = "test_repo"
    # Remove useless file
    remove_files_by_extension(TEMPLATE_DIR,".yaml")
    remove_files_by_extension(TEMPLATE_DIR,".yml")
    remove_file_by_name(TEMPLATE_DIR,"Dockerfile.develop")
    remove_file_by_name(TEMPLATE_DIR,"nuget-dev.config")
    remove_file_by_name(TEMPLATE_DIR,"nuget-sazman.config")
    remove_file_by_name(TEMPLATE_DIR,"nuget.config")
    print("cleaned the useless files.")



def rename_dot_net_template(new_name = "pool"):
    TEMPLATE_DIR = "test_repo"
    placeholder = "rpk.saja.template."
    new_string = "rpk.saja.cad.{}.".format(new_name)
    print("Starting renaming process")
    rename_files_and_dirs(TEMPLATE_DIR,placeholder,new_string)


def replace_content(new_name = "pool"):
    TEMPLATE_DIR = "test_repo"
    old_string = "rpk.saja.template."
    new_string = "rpk.saja.cad.{}.".format(new_name)
    print("Starting renaming process")
    replace_content_in_files(TEMPLATE_DIR,old_string,new_string)


def get_cicd_template():
    TEMPLATE_URL = "ssh://azurenew.rpk.ir:22/tfs/RPKavoshDevOps/SAJAK/_git/rpk-saja-template-cicd-dotnet"
    GIT_DIR = "test_repo"
    git = GitManager(GIT_DIR)
    git.clone_repo(TEMPLATE_URL,GIT_DIR)
    git.checkout_branch("develop")
    print("Template is downloaded successfully.")

    

def create_repo(repo_name):
    az



if __name__ == "__main__":
    get_dot_net_template()
    clean_dot_net_template()
    rename_dot_net_template()
    replace_content()
