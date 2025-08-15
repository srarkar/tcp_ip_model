MAINCLASS = Server
JARFILE = $(MAINCLASS).jar
LIBDIR = lib
LIBJAR = $(LIBDIR)/exp4j-0.4.8.jar
SRC = $(MAINCLASS).java
CLASS = $(MAINCLASS).class

# default: build everything
all: $(JARFILE)

# compile when Server.java is newer than Server.class (e.g. recently updated)
$(CLASS): $(SRC)
	@javac -cp $(LIBJAR) $(SRC) 
	@echo "$(SRC) compiled successfully"

# build JAR if .class or MANIFEST/lib change
$(JARFILE): $(CLASS) MANIFEST.MF $(LIBJAR)
	@jar cfm $(JARFILE) MANIFEST.MF $(CLASS) -C $(LIBDIR) $(notdir $(LIBJAR)) 
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
