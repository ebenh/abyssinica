# Contributing

## Code of Conduct

Before contributing, please take time to review our code of conduct [here](CODE_OF_CONDUCT.md).

## Developer Cookbook

### Publishing to PyPI
1. Update `MANIFEST.in` to include any new non-source files you may have added.
2. Manually increment the version number by editing `setup.cfg`
3. Tag the release. The value of `${VERSION}` should be of the form `v1.0.0`.
    
        git tag ${VERSION} && git push --tags

4. Build the Python package 

        python setup.py sdist

5. Install/upgrade `twine`

        python3 -m pip install --upgrade twine

6. Upload to the PyPI test repository. For the username, use `__token__`. For the password, use your token value, 
including the `pypi-` prefix.

        python3 -m twine upload --repository testpypi dist/*

7. Test the package.
        
        virtualenv venv
        source venv/bin/activate
        python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps abyssinica
        python3 -c "from abyssinica.numerals import arabic_to_geez; print(arabic_to_geez(42));"
        deactivate

8. If the above commands execute without errors, upload you're ready to upload the  library to PyPI. For the username, 
use `__token__`. For the password, use your token value, including the `pypi-` prefix.

        python3 -m twine upload dist/*

9. Optionally, clean your working tree.

        git clean -idx