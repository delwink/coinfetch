EXEC=coinfetch
PREFIX=/usr/local

install:
	install -D -m755 $(EXEC) $(DESTDIR)$(PREFIX)/bin/$(EXEC)
