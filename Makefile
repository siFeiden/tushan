help :
	@echo "make protocol"
	@echo ">> builds protocol specifications"

.DEFAULT: help

.PHONY: protocol

PROTSRC=protocol/
protocol :
	@echo "making protocol specifications"
	$(MAKE) -C $(PROTSRC)
