#include <stdio.h>
#include <string.h>
#include <stdlib.h>


void main() {
    printf("Hello World\n");
    
    // Allocate a small block
    char *buffer = (char *)malloc(32);
    if (!buffer) {
        printf("malloc failed!\n");
        return;
    }

    printf("malloc succeeded! Address: %p\n", buffer);

    // Fill the memory and print it
    strcpy(buffer, "Hello from malloc!");
    printf("Buffer content: %s\n", buffer);

    // Free is a no-op in minimal embedded systems but call it anyway
    free(buffer);

    printf("Test complete.\n");

    return;
}