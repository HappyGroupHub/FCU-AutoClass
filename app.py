"""This python file will do the AutoClass job."""

import utilities as utils

config = utils.read_config()

print(config.get('username'))
print(config.get('password'))
