# Compiler and tools for RISC-V (xPack toolchain)
CC = riscv-none-elf-gcc
AS = riscv-none-elf-as
LD = riscv-none-elf-ld
OBJDUMP = riscv-none-elf-objdump
OBJCOPY = riscv-none-elf-objcopy

# Compiler flags
CFLAGS = -march=rv32imf -mabi=ilp32f -O2 -Wall -Wextra
CFLAGS += -I./include
CFLAGS += -fno-builtin -nostdlib -nostartfiles
CFLAGS += -g

# Assembler flags
ASFLAGS = -march=rv32imf -mabi=ilp32f

# Linker flags
LDFLAGS = -march=rv32imf -mabi=ilp32f

# Directories
SRC_DIR = src
INC_DIR = include
BUILD_DIR = build
BIN_DIR = bin

# Source files
C_SOURCES = $(wildcard $(SRC_DIR)/*.c)
ASM_SOURCES = $(wildcard $(SRC_DIR)/*.S)

# Object files
C_OBJECTS = $(patsubst $(SRC_DIR)/%.c, $(BUILD_DIR)/%.o, $(C_SOURCES))
ASM_OBJECTS = $(patsubst $(SRC_DIR)/%.S, $(BUILD_DIR)/%.o, $(ASM_SOURCES))
OBJECTS = $(C_OBJECTS) $(ASM_OBJECTS)

# Output binary
TARGET = $(BIN_DIR)/bci_system.elf
TARGET_BIN = $(BIN_DIR)/bci_system.bin
TARGET_HEX = $(BIN_DIR)/bci_system.hex

# Default target
all: directories $(TARGET) $(TARGET_BIN) disassemble

# Create necessary directories
directories:
	@mkdir -p $(BUILD_DIR)
	@mkdir -p $(BIN_DIR)

# Compile C source files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	@echo "Compiling $<..."
	$(CC) $(CFLAGS) -c $< -o $@

# Assemble assembly files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.S
	@echo "Assembling $<..."
	$(AS) $(ASFLAGS) $< -o $@

# Link all object files
$(TARGET): $(OBJECTS)
	@echo "Linking..."
	$(CC) $(LDFLAGS) -o $@ $^ -lm

# Create binary file
$(TARGET_BIN): $(TARGET)
	@echo "Creating binary..."
	$(OBJCOPY) -O binary $< $@

# Create hex file
$(TARGET_HEX): $(TARGET)
	@echo "Creating hex file..."
	$(OBJCOPY) -O ihex $< $@

# Disassemble for inspection
disassemble: $(TARGET)
	@echo "Creating disassembly..."
	$(OBJDUMP) -d $(TARGET) > $(BIN_DIR)/bci_system.asm

# Run with QEMU (RISC-V 32-bit)
run: all
	@echo "Running on QEMU RISC-V..."
	qemu-system-riscv32 -machine virt -nographic -bios none -kernel $(TARGET)

# Run with Spike ISA simulator
spike: all
	@echo "Running on Spike..."
	spike --isa=rv32imf $(TARGET)

# Clean build artifacts
clean:
	@echo "Cleaning..."
	rm -rf $(BUILD_DIR) $(BIN_DIR)

# Clean and rebuild
rebuild: clean all

# Show file sizes
size: $(TARGET)
	riscv-none-elf-size $(TARGET)

# Help target
help:
	@echo "RISC-V BCI System Makefile"
	@echo "=========================="
	@echo "Targets:"
	@echo "  all        - Build the complete system (default)"
	@echo "  run        - Run on QEMU RISC-V simulator"
	@echo "  spike      - Run on Spike ISA simulator"
	@echo "  clean      - Remove all build artifacts"
	@echo "  rebuild    - Clean and rebuild"
	@echo "  size       - Show binary size information"
	@echo "  disassemble- Generate disassembly listing"
	@echo "  help       - Show this help message"

.PHONY: all directories clean rebuild run spike size disassemble help
