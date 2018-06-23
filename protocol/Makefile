.PHONY: clean rebuild

PDFNAME=spec.pdf
PDFPATH=../$(PDFNAME)

SRCFILE=$(patsubst %.pdf, %.tex, $(PDFNAME))

BUILDDIR=build

LATEXCMD=latexmk

LATEXFLAGS=-shell-escape -output-directory=$(BUILDDIR) -interaction=nonstopmode -pdf

$(PDFPATH): $(SRCFILE)
	mkdir -p $(BUILDDIR)
	pipenv run $(LATEXCMD) $(LATEXFLAGS) $(SRCFILE)
	cp $(BUILDDIR)/$(PDFNAME) $(PDFPATH)

clean:
	rm -r $(BUILDDIR)
	rm -f $(PDFPATH)

rebuild: clean
	$(MAKE)

