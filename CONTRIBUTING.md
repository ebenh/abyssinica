# Contributing

## Code of Conduct

Before contributing, please take time to review our code of conduct [here](CODE_OF_CONDUCT.md).

## Developer Cookbook

### Cloning the Git Repository

    $ git clone https://github.com/ebenh/abyssinica/ abyssinica

### Publishing to PyPI
1. Update `MANIFEST.in` to include any new non-source files you may have added.
2. Manually increment the version number in `setup.cfg`.
3. Build the Python package. 

        $ python setup.py sdist

4. Install/upgrade `twine`.

        $ python3 -m pip install --upgrade twine

5. Upload to the PyPI test repository. For the username use `__token__`. For the password use your token for the test 
repository, making sure to include the `pypi-` prefix.

        $ python3 -m twine upload --repository testpypi dist/*

6. Test the uploaded package.
        
        $ virtualenv venv
        $ source venv/bin/activate
        $ python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps abyssinica
        $ python3 -c "from abyssinica.numerals import arabic_to_geez; print(arabic_to_geez(42));"
        $ deactivate

7. Tag the release. The value of `${VERSION}` should be of the form `v1.0.0`.
    
        $ git tag ${VERSION} && git push --tags

8. If the above commands execute without errors, you're ready to upload the library to PyPI. For the username use 
`__token__`. For the password use your token, making sure to include the `pypi-` prefix.

        $ python3 -m twine upload dist/*

9. Optionally, clean your working tree.

        $ git clean -idx
