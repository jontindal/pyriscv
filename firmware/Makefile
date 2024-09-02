ARCH = rv32i
ABI = ilp32

TARGET = basic_asm

BUILD_DIR = build
LINKER_FILE = sections.lds

PREFIX = riscv32-unknown-elf-

CC = $(PREFIX)gcc
AS  = $(PREFIX)as
RL = $(PREFIX)ranlib
LD  = $(PREFIX)ld
OC  = $(PREFIX)objcopy
OD  = $(PREFIX)objdump
CPP = $(PREFIX)cpp

CC_FLAGS = -march=$(ARCH) -mabi=$(ABI) -static -mcmodel=medany -fvisibility=hidden -nostdlib -nostartfiles -T $(LINKER_FILE)
OCFLAGS = --strip-all -O binary
ODFLAGS = -D

all: $(BUILD_DIR)/$(TARGET).hex $(BUILD_DIR)/$(TARGET).elf $(BUILD_DIR)/$(TARGET)-dump.txt $(BUILD_DIR)/$(TARGET).bin

$(BUILD_DIR)/%.hex: $(BUILD_DIR)/%.bin
	hexdump -ve '1/4 "%08x\n"' $< > $@

$(BUILD_DIR)/%.bin: $(BUILD_DIR)/%.elf
	$(OC) $(OCFLAGS) $< $@

$(BUILD_DIR)/%-dump.txt: $(BUILD_DIR)/%.elf
	$(OD) $(ODFLAGS) $< > $@

$(BUILD_DIR)/%.elf: %.S start.S | $(BUILD_DIR)
	$(CC) $(CC_FLAGS) -o $@ $^

$(BUILD_DIR)/%.elf: %.c start.S | $(BUILD_DIR)
	$(CC) $(CC_FLAGS) -o $@ $^

$(BUILD_DIR):
	mkdir --parents $@

clean:
	rm -rf $(BUILD_DIR)
