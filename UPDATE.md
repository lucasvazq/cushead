1) Change the version in ['setup.py'](./setup.py)

2) Commit git:

    `git add . && git commit -m 'new version' && git push origin master`

3) Update to Twine

    `twine upload --skip-existing dist/*`

4) Upgrade package in machine:

    `pip install cushead.py --upgrade`
