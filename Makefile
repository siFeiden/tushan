help :
	@echo "make protocol"
	@echo ">> builds protocol specifications"

.DEFAULT: help

.PHONY: protocol watch

PROTSRC=protocol/
protocol :
	@echo "making protocol specifications"
	$(MAKE) -C $(PROTSRC)

watch :
	$(MAKE) -C $(PROTSRC) watch
