1) Change the version in ['setup.py'](./setup.py)

2) Commit git:

    `git add . && git commit -m 'new version' && git push origin master`

3) Create new package

    `python3 setup.py sdist`

4) Upload to PYPI using twine

    `twine upload --skip-existing dist/*`

5) Upgrade package in machine:

    `python3 -m pip install cushead.py --upgrade`
