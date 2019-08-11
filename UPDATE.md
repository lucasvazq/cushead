1) Change the version in ['setup.py'](./setup.py)

2) Edit version in logo.xcf and logo.png

3) Build the new package

    `python3 setup.py sdist`

4) Add to git:

    `git add . && git commit -m 'new version' && git push origin master`

5) Upload to PYPI using twine

    `twine upload --skip-existing dist/*`

6) Upgrade package in machine:

    `python3 -m pip install cushead.py --upgrade`

7) Test

    `python3 cushead.py -h`
