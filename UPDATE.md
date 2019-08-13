# Steps for upgrade the package

## 1 - Change the version in

['./_info.py'](./_info.py)

['./README.md](./README.md)

['./logo.xcf'](./logo.xcf)

['./logo.png'](./logo.png)

## 2 - Remove old packages deleting the next folders

['./cushead.py.egg-info/'](./cushead.py.egg-info/.)

['./dist/'](./dist/.)

`rm -rf ./cushead.py.egg-info/ ./dist/`

## 3 - Build the new package

`python3 ./setup.py sdist`

## 4 - Remove all python cache files

`find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf`

## 5 - Add to git

`git add . && git commit -m 'new version' && git push origin master`

## 6 - Upload to PYPI using twine

`twine upload --skip-existing dist/*`

## - 7 Upgrade package in machine

`python3 -m pip install cushead.py --upgrade`

## - 8 Test

`python3 cushead.py -h`

