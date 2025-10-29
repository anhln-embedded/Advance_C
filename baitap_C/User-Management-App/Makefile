# Tên file thực thi
TARGET := program

# Thư mục chứa source và output
SRC_DIRS := App Service UI
OBJ_DIR := build

# Tìm tất cả file .c trong các thư mục SRC_DIRS
SRCS := $(wildcard $(addsuffix /*.c, $(SRC_DIRS)))

# Chuyển đổi đường dẫn file .c → file .o trong OBJ_DIR
OBJS := $(patsubst %.c, $(OBJ_DIR)/%.o, $(SRCS))

# Compiler và flags
CC := gcc
CFLAGS := -g -Wall -Wextra -Werror  -std=c17 -IApp -IService -IStructure -IUI

# Quy tắc build
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $@
run:
	./$(TARGET)

# Quy tắc compile .c → .o (tạo thư mục build tương ứng nếu chưa có)
$(OBJ_DIR)/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c $< -o $@

# Dọn dẹp
clean:
	rm -rf $(OBJ_DIR) $(TARGET)

.PHONY: all clean
