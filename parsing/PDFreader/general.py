import os


# Each website is a separate project (folder)
def create_project_dir(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


# Create queue and crawled files (if not created)
def create_data_files(project_name, file_name):
    create_project_dir(project_name)
    file = os.path.join(project_name, file_name)
    if not os.path.isfile(file):
        write_file(file, '')


# Create a new file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


def get_path(project_name, file_name):
    return "./"+project_name+"/" + file_name

