help:
	@echo "make help            	- Prints this help message"
	@echo "make flake8				- Test flake8			  "
	@echo "make mypy				- Test mypy			  	  "
	@echo "make pytest				- Test with pytest			  	  "


flake8:
	flake8 lefaso_net_scraper


mypy:
	mypy lefaso_net_scraper


pytest:
	pytest tests
