import getpass
import os.path
import yaml

config_file = 'configs.yml'

"""
Get the user's login information from "configs.yml" if it exists,
otherwise ask the user for the information from the command line.
"""
def get_login_information():

    configs = {}

    if not os.path.isfile(config_file):
        configs['email'] = raw_input('Laracasts.com email: ')
        configs['password'] = getpass.getpass('Laracasts.com password: ')
        configs['output_file'] = raw_input('Output file path: ')

        write_configs(configs)

    else: configs = get_configs()
    return configs['email'], configs['password']


"""
Gets the name of the output file from our configuration file.
"""
def get_output_filename():
    configs = get_configs()
    return configs['output_file']


"""
Read the configuration options from the YAML file.
"""
def get_configs():
    with open(config_file, 'r') as file_stream:
        configs = yaml.load(file_stream)

    return configs


"""
Write the given configuration information as a dict into
the configuration YAML file, so we can store the information for later.
"""
def write_configs(configs):
    with open(config_file, 'w') as file_stream:
        data = yaml.dump(configs, default_flow_style=False)
        file_stream.write(data)

