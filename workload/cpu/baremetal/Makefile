CC=riscv64-unknown-elf-gcc
SPIKE=spike
Verilator=spike

# $(CI_PROJECT_PATH) 是环境变量,表示chipyard的路径
PROJECT_PATH=$(CI_PROJECT_PATH)
ZIPPER_PATH=$(CI_ZIPPER_PATH)
CONFIG=CustomGemminiSoCConfig

BUILD_DIR=$(abspath ./build)
CSR_PATH=$(abspath ./)
INC_PATH=$(abspath ./include)

CFLAGS=-std=c11 -g -fno-common -O2 -static -fno-builtin-printf -specs=htif_nano.specs
LDFLAGS=

INCFLAGS=$(addprefix -I, $(INC_PATH))
CFLAGS+=$(INCFLAGS)
# spike 的参数，如gemmini需要 --extension=gemmini 
SPIKE_EXT= 


$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

hello-bin: $(BUILD_DIR)
	@$(CC) -o $(BUILD_DIR)/$@ $(CSR_PATH)/hello.c $(CFLAGS) $(LDFLAGS)

hello-spike-run: hello-bin
	@$(SPIKE) $(SPIKE_EXT) $(BUILD_DIR)/$<

hello-verilator-run: hello-bin
	$(ZIPPER_PATH)/sims/verilator/simulator-chipyard.harness-$(CONFIG) +permissive +loadmem=$(BUILD_DIR)/$< +loadmem_addr=80000000 +permissive-off $(BUILD_DIR)/$< 


clean:
	rm -rf $(BUILD_DIR)

.PHONY: hello-bin hello-spike-run hello-verilator-run clean


