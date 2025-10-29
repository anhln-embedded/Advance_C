# Tên chương trình
TARGET = run

# Thư mục chứa các file .h và .c
SOURCE_DIRS = App/src
HEADER_DIRS = App/inc
BINARY_DIR = bin
CSV_DIR = database

# Lấy tất cả file .c từ các thư mục trên
vpath %.c $(SOURCE_DIRS)
SOURCES = $(foreach dir,$(SOURCE_DIRS),$(wildcard $(dir)/*.c))
OBJECTS = $(patsubst %.c,$(BINARY_DIR)/%.o,$(notdir $(SOURCES)))
CSV_FILE = $(CSV_DIR)/thongtin.csv

# Compiler & flags
CC = gcc
CFLAGS = -g -Wall -Wextra -Werror -std=c17 \
         $(foreach dir,$(HEADER_DIRS),-I$(dir))

# Quy tắc mặc định (biên dịch tự động ra tệp thực thi)
all: $(BINARY_DIR)/$(TARGET)

# Tạo thư mục bin nếu chưa có
$(BINARY_DIR): 
	mkdir -p $(BINARY_DIR)

# Link các object thành chương trình
$(BINARY_DIR)/$(TARGET): $(OBJECTS) | $(BINARY_DIR) 
	@echo "Linking..."
	$(CC) $(CFLAGS) -o $@ $^

# Build từng .c thành .o
$(BINARY_DIR)/%.o: %.c | $(BINARY_DIR)
	@echo "Compiling $<..."
	$(CC) $(CFLAGS) -c -o $@ $<

# Chạy chương trình
run: 
	./$(BINARY_DIR)/$(TARGET)

# Dọn sạch
clean:
	rm -rf $(BINARY_DIR)/*.o $(BINARY_DIR)/$(TARGET)

.PHONY: all clean run
