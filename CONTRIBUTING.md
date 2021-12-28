# Contributing

## Code of Conduct

Before contributing, please take time to review our code of conduct [here](CODE_OF_CONDUCT.md).

## Developer Cookbook

### Cloning the Git Repository

    $ git clone https://github.com/ebenh/abyssinica/ abyssinica

### Publishing to PyPI

1. Update `MANIFEST.in` to include any new, non-source files you may have added.
2. Manually increment the version number in `setup.cfg`.
3. Build the Python package. 

        $ python setup.py sdist

4. Install and/or upgrade `twine`.

        $ python3 -m pip install --upgrade twine

5. Upload the package to the PyPI test repository.

        $ python3 -m twine upload --repository testpypi dist/*

   > Note: Username is `__token__` and password is your token for the test repository (make sure to include the `pypi-` 
   > prefix).

6. Test the package you just uploaded to the PyPI test repository.
        
        $ virtualenv venv
        $ source venv/bin/activate
        $ python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps abyssinica
        $ python3 -c "from abyssinica.numerals import arabic_to_geez; print(arabic_to_geez(42));"
        $ deactivate

7. If the above commands complete without errors, upload the library to PyPI.

        $ python3 -m twine upload dist/*

   > Note:  Username is `__token__` and password is your PyPI token (make sure to include the `pypi-` prefix).

8. Tag the release. The value of `${VERSION}` should be the package's semantic version prefixed with a "v" (e.g. 
`v1.0.0`).
    
        $ git tag ${VERSION} && git push --tags

9. Optionally, clean your working tree.

        $ git clean -idx
