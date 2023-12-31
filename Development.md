# Development for cxxbuild

If you want to help or adjust the python cxxbuild library, please follow these instructions.

### Versioning requirements

`pip install bumpver`

`bumpver update --patch`


## How to test locally (devs only)

Execute all demos for all platforms.

## Packaging instructions

Adapted from OptFrame python project.

Edit `pyproject.toml`.

`# apt install python3.10-venv`
`
`virtualenv venv`

`source venv/bin/activate`

`python3 -m pip install pip-tools`

`pip-compile pyproject.toml`

`pip-sync`

For versioning:

`python3 -m pip install bumpver`

`bumpver init`

**To increase PATCH number:**

`bumpver update --patch`

Clean existing dist folder:

`rm -f dist/*`

Build and check:

`python3 -m pip install build twine`

`rm -f dist/* && python3 -m build`

`twine check dist/*`

Remove .whl to prevent error:

`rm -f dist/*.whl`

Update on test repository (not working fine for now):

`twine upload -r testpypi dist/* --verbose`

Test if OK on test package website:

`python3 -m pip install -i https://test.pypi.org/simple cxxbuild --upgrade`

Finally, update to main repository:

`twine upload dist/*`

`python3 -m pip install cxxbuild --upgrade`

Thanks again to: https://realpython.com/pypi-publish-python-package/

