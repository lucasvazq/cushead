1) Change the version in:

['_info.py'](./_info.py)

['README.md](./README.md)

['logo.xcf'](./logo.xcf)

['logo.png'](./logo.png)

2) Build the new package

    `python3 setup.py sdist`

3) Add to git:

    `git add . && git commit -m 'new version' && git push origin master`

4) Upload to PYPI using twine

    `twine upload --skip-existing dist/*`

5) Upgrade package in machine:

    `python3 -m pip install cushead.py --upgrade`

6) Test

    `python3 cushead.py -h`
