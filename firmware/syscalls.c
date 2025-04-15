#include <sys/types.h>
#include <sys/stat.h>
#include <stdint.h>

#define UART_ADDR 0xa0000000

int _write(int file, char *ptr, int len) {
    volatile char* uart = (char*)UART_ADDR;

    for (int i = 0; i < len; i++) {
        *uart = ptr[i];
    }
    return len;
}

extern char _sheap;  // Start of heap
extern char _eheap;

static char *heap_end = 0;

void* _sbrk(ptrdiff_t incr) {
    char *prev_heap_end;

    if (heap_end == 0) {
        heap_end = &_sheap;
    }

    prev_heap_end = heap_end;

    // Optional safety check: stop heap from growing into stack
    if ((heap_end + incr) > &_eheap) {
        // Out of memory
        return (void *)-1;
    }

    heap_end += incr;
    return (void *)prev_heap_end;
}

// Optional stubs
int _read(int file, char *ptr, int len) { return 0; }
int _close(int file) { return -1; }
int _fstat(int file, struct stat *st) {
    st->st_mode = S_IFCHR;
    return 0;
}
int _isatty(int file) { return 1; }
int _lseek(int file, int ptr, int dir) { return 0; }

void _exit(int status) {
    while (1);  // Trap here if needed
}

void _kill(int pid, int sig) {}
int _getpid() { return 1; }
