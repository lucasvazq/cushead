# Steps for upgrade the package

## 1 - Change the version in

['./README.md](./README.md)

['./doc/logo.xcf'](./doc/logo.xcf)

['./doc/logo.png'](./doc/logo.png)

['./src/presentation.png'](./doc/presentation.png)

['./src/info.py'](./src/info.py)

## 2 - Remove old packages deleting the next folders

['./cushead.egg-info/'](./cushead.egg-info/.)

['./dist/'](./dist/.)

`rm -rf ./cushead.egg-info/ ./dist/`

## 3 - Build the new package

`python3 ./setup.py sdist bdist_wheel`

## 4 - Remove all python cache files

`find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf`

## 5 - Add to git

`git add . && git commit -m 'new version' && git push origin master`

## 6 - Upload to PYPI using twine

`twine upload --skip-existing dist/*`

## - 7 Upgrade package in machine

`cd .. && python3 -m pip install cushead --upgrade`

## - 8 Test

`cushead -h`
