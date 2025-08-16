MAINCLASS = Server
JARFILE = $(MAINCLASS).jar
LIBDIR = lib
LIBJARS := $(wildcard $(LIBDIR)/*.jar)
SRC = $(MAINCLASS).java
CLASS = $(MAINCLASS).class

# default: build everything
all: $(JARFILE)

# compile when Server.java is newer than Server.class (e.g. recently updated)
$(CLASS): $(SRC)
	@javac -cp "$(LIBJARS: =:)" $(SRC)
	@echo "$(SRC) compiled successfully"

# build class if manifest or jar files change
$(JARFILE): $(CLASS) MANIFEST.MF $(LIBJARS)
	@jar cfm $(JARFILE) MANIFEST.MF $(CLASS)
	@echo "$(JARFILE) built successfully"

# run JAR
run: $(JARFILE) # depends on jar file existing
	@echo "Running $(JARFILE)..."
	@java -jar $(JARFILE) || test $$? -eq 130 

# remove .class and .jar file. "-f" will ignore errors if already removed
clean:
	@if [ -f $(CLASS) ]; then \
		rm -f $(CLASS); \
		echo "$(CLASS) has been deleted"; \
	else \
		echo "$(CLASS) does not exist"; \
	fi 

	@if [ -f $(JARFILE) ]; then \
		rm -f $(JARFILE); \
		echo "$(JARFILE) has been deleted"; \
	else \
		echo "$(JARFILE) does not exist"; \
	fi 
