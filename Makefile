help :
	@echo "make protocol"
	@echo ">> builds protocol specifications"

.DEFAULT: help

.PHONY: protocol watch

PROTSRC=protocol/
protocol :
	@echo "making protocol specifications"
	pipenv run $(MAKE) -C $(PROTSRC)

watch :
	pipenv run $(MAKE) -C $(PROTSRC) watch
