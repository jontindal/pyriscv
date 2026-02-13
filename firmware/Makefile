ARCH = rv32i
ABI = ilp32
USE_STDLIB = 1

TARGET ?= sort

SRCS = $(TARGET).c \
	sort_func.S

BUILD_DIR = build
LINKER_FILE = sections.lds

PREFIX = riscv-none-elf-

CC = $(PREFIX)gcc
AS  = $(PREFIX)as
RL = $(PREFIX)ranlib
LD  = $(PREFIX)ld
OC  = $(PREFIX)objcopy
OD  = $(PREFIX)objdump
CPP = $(PREFIX)cpp

CC_FLAGS = -march=$(ARCH) -mabi=$(ABI)
LD_FLAGS = -static -mcmodel=medany -nostartfiles -T $(LINKER_FILE)
LD_FLAGS += -Wl,--gc-sections -Wl,--print-memory-usage
OCFLAGS = --strip-all -O binary
ODFLAGS = -D
ifdef USE_STDLIB
	CC_FLAGS += --specs=nosys.specs
	SRCS += syscalls.c
else
	CC_FLAGS += -nostdlib
endif

SRCS += start.S
OBJS = $(addprefix $(BUILD_DIR)/, \
	$(patsubst %.S,%.o, \
	$(patsubst %.c,%.o,$(SRCS))))

all: $(BUILD_DIR)/$(TARGET).elf $(BUILD_DIR)/$(TARGET)-dump.txt $(BUILD_DIR)/$(TARGET).bin

$(BUILD_DIR)/$(TARGET).bin: $(BUILD_DIR)/$(TARGET).elf
	$(OC) $(OCFLAGS) $< $@

$(BUILD_DIR)/$(TARGET)-dump.txt: $(BUILD_DIR)/$(TARGET).elf
	$(OD) $(ODFLAGS) $< > $@

$(BUILD_DIR)/$(TARGET).elf: $(OBJS) | $(BUILD_DIR)
	$(CC) $(CC_FLAGS) $(LD_FLAGS) -o $@ $^

$(BUILD_DIR)/%.o: %.c | $(BUILD_DIR)
	$(CC) $(CC_FLAGS) -c -o $@ $<

$(BUILD_DIR)/%.o: %.S | $(BUILD_DIR)
	$(CC) $(CC_FLAGS) -c -o $@ $<

$(BUILD_DIR):
	mkdir --parents $@

clean:
	rm -rf $(BUILD_DIR)
