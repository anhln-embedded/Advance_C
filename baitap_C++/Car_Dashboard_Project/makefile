# Compiler and flags
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -I./App/Inc -I./Data -I./UI -I./Server -I./Server/cpp-httplib

# Directories
SRC_DIR_MAIN = ./App/Src
DATA_DIR = ./Data
SRC_DIR_SERVER = ./Server
BIN_DIR = ./bin

# Libraries for Windows
LIBS = -lws2_32

# Sources and Objects for Main
SOURCES_MAIN = $(wildcard $(SRC_DIR_MAIN)/*.cpp) $(wildcard $(DATA_DIR)/*.cpp)
OBJECTS_MAIN = $(patsubst $(SRC_DIR_MAIN)/%.cpp, $(BIN_DIR)/%.o, $(filter $(SRC_DIR_MAIN)/%.cpp, $(SOURCES_MAIN))) \
               $(patsubst $(DATA_DIR)/%.cpp, $(BIN_DIR)/%.o, $(filter $(DATA_DIR)/%.cpp, $(SOURCES_MAIN)))

# Sources and Objects for Server
SOURCES_SERVER = $(SRC_DIR_SERVER)/Server.cpp
OBJECTS_SERVER = $(BIN_DIR)/Server.o

# Lấy đường dẫn tuyệt đối tới file main.exe
TARGET_PATH := $(shell cd)

# Output binaries
OUTPUT_MAIN = $(BIN_DIR)/Car.exe
OUTPUT_SERVER = $(BIN_DIR)/Server.exe

# Default target: build main only
main: $(OUTPUT_MAIN)

$(OUTPUT_MAIN): $(OBJECTS_MAIN)
	mkdir -p $(BIN_DIR)
	$(CXX) $(CXXFLAGS) -o $@ $^

$(BIN_DIR)/%.o: $(SRC_DIR_MAIN)/%.cpp
	mkdir -p $(BIN_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(BIN_DIR)/%.o: $(DATA_DIR)/%.cpp
	mkdir -p $(BIN_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Server target: build and run server
server: clean_server $(OUTPUT_SERVER)
	start powershell -NoExit -Command "cd '$(TARGET_PATH)'; ./$(OUTPUT_SERVER); pause"

$(OUTPUT_SERVER): $(OBJECTS_SERVER)
	mkdir -p $(BIN_DIR)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LIBS)

$(BIN_DIR)/%.o: $(SRC_DIR_SERVER)/%.cpp
	mkdir -p $(BIN_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Run main: clean -> build main -> run main
run: clean_main main
	./$(OUTPUT_MAIN)

# Run both main and server: clean -> build both -> run both
all: clean main $(OUTPUT_SERVER)
	start powershell -NoExit -Command "cd '$(TARGET_PATH)'; ./$(OUTPUT_SERVER); pause"
	./$(OUTPUT_MAIN)

# Clean only main-related files
clean_main:
	rm -f $(OBJECTS_MAIN) $(OUTPUT_MAIN)

# Clean only server-related files
clean_server:
	rm -f $(OBJECTS_SERVER) $(OUTPUT_SERVER)

# Clean all compiled files
clean: clean_main clean_server

# Phony targets
.PHONY: all main server run clean clean_main clean_server
