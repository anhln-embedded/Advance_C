# Tên của chương trình
TARGET = main

# Thư mục chứa header và source files
HEADER_DIR = inc
SOURCE_DIRS = src


# Các tệp nguồn và tệp object tương ứng
#SOURCES  =$(wildcard $(SOURCE_DIR)/*.c)
SOURCES = $(foreach dir, $(SOURCE_DIRS), $(wildcard $(dir)/*.c))

OBJECTS = $(SOURCES:.c=.o)

# Trình biên dịch và các cờ
CC =gcc
CFLAGS = -I$(HEADER_DIR) -Wall -Wextra

# Quy tắc đầu tiên là quy tắc mặc định sẽ được thực thi
all: $(TARGET)

# Quy tắc để tạo ra tệp thực thi
$(TARGET): $(OBJECTS)
	@echo "Compiling $(TARGET) with objects: $(OBJECTS)"
	$(CC) -o $@ $^

# Quy tắc để biên dịch các tệp .cpp thành .o
$(SOURCE_DIR)/%.o: $(SOURCE_DIR)/%.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(TARGET): $(OBJECTS) $(CSV_FILE)
	$(CC) $(OBJECTS) -o $(TARGET)

# Quy tắc để làm sạch thư mục build
clean:
	rm -f $(SOURCE_DIR)/*.o $(TARGET)

run: 
	$(TARGET)
	./$(TARGET)
# Quy tắc giả (phony target)
.PHONY: all clean
