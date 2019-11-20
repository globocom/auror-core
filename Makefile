.PHONY: clean release

ROOT_PATH=$(shell pwd)

clean:
	-@rm -rf $(ROOT_PATH)/*.egg-info
	-@rm -rf $(ROOT_PATH)/dist
	-@rm -rf $(ROOT_PATH)/build

release: clean

ifndef VERSION
	@echo "need VERSION=xxx"
else
	@echo $(VERSION) > version.txt
	@git tag $(VERSION)
	@git commit version.txt -m "Bump $(VERSION)"
	@git push --tags
	@git push origin HEAD
	@python setup.py sdist
	@twine upload dist/*
endif

pep8format:
	autopep8 -ri -a -a ./auror_core

verifypep8:
	find ./auror_core -name \*.py -exec pycodestyle {} +

test:
	@python -m unittest discover
