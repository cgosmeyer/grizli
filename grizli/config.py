"""
Set default paths, etc.
All grizli modules should read from this.
No paths anywhere else should be coded.

Use
---
	# Example within grizli 
	from . import config
	path_raw = config.PATH_RAW

	# Example if using in your own pipeline
	from grizli import config
	path_raw = config.PATH_RAW
"""

PATH_RAW = '../RAW'
PATH_PERSISTENCE = '../Persistence'
PATH_LOGS = '../logs'
