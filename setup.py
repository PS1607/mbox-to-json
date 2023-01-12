from setuptools import setup, find_packages

with open('requirements.txt') as f:
	requirements = f.readlines()

long_description = 'A small package that converts MBOX files to JSON. Also includes functionality to extract attachments.'

setup(
		name ='mbox-to-json',
		version ='0.0.1',
		author ='Prakhar Sharma',
		author_email ='prakharsharma1607@gmail.com',
		url ='https://github.com/PS1607/mbox-to-json',
		description ='MBOX to JSON Converter',
		long_description = long_description,
		long_description_content_type ="text/markdown",
		license ='MIT',
		packages = find_packages(),
		entry_points ={
			'console_scripts': [
				'mbox-to-json = src.main:main'
			]
		},
		classifiers =(
			"Programming Language :: Python :: 3",
			"License :: OSI Approved :: MIT License",
			"Operating System :: OS Independent",
		),
		keywords ='MBOX to JSON Converter',
		install_requires = requirements,
		zip_safe = False
)