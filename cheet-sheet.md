# Pipenv: 26-06-2022
- Install pipenv: pip install pipenv
- Activate venv: pipenv shell
- Run in venv without launching a shell: pipenv run <command>
- General installs: pipenv install <package>
- Installing for dev only: pipenv install <pakage> --dev
- Lock environment: pipenv lock
- Install from Pipfile: pipenv install --dev
- Install from .lock: pipenv install --ignore-pipfile
- Uninstall a package: pipenv uninstall <package>
- Uninstall all packages: pipenv uninstall --all
- Uninstall dev packages only: pipenv uninstall --all-dev
- Check for security vulnerabilities: pipenv check
- Find where the virtual env is: pipenv --venv
- Find where the project home is: pipenv --where
- Open a package in the default editor: pipenv open flask
- Show dependecy graph: pipenv graph
- Show reverse dependecy graph: pipenv graph --reverse


# H1
## H2
### H3
Bold	**bold text**
Italic	*italicized text*
Blockquote	> blockquote
Ordered List	1. First item
Unordered List	- First item
Code	`code`
Horizontal Rule	---
Link	[title](https://www.example.com)
Image	![alt text](image.jpg)
Task List	- [x] Write the press release
- [ ] Update the website