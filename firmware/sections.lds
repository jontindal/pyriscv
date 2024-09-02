/* Generate a link error if heap and stack don't fit into RAM */
__heap_size    	= 0x200;  /* required amount of heap */
__stack_size	= 0x800;  /* required amount of stack */


MEMORY {
	RAM (xrw)		: ORIGIN = 0x90000000, LENGTH = 4K
	FLASH (rx)		: ORIGIN = 0x80000000, LENGTH = 32K
}


SECTIONS {

	/* The program code and other data goes into FLASH */
    .text :
    {
        . = ALIGN(4);
		KEEP(*(._start)) 	/* Startup code */
        *(.text)           	/* .text sections (code) */
        *(.text*)          	/* .text* sections (code) */
        *(.rodata)         	/* .rodata sections (constants, strings, etc.) */
        *(.rodata*)        	/* .rodata* sections (constants, strings, etc.) */
        *(.srodata)        	/* .rodata sections (constants, strings, etc.) */
        *(.srodata*)       	/* .rodata* sections (constants, strings, etc.) */
        . = ALIGN(4);
        _etext = .;        	/* define a global symbol at end of code */
        _sidata = _etext;  	/* This is used by the startup in order to initialize the .data secion */
    } >FLASH

    /* This is the initialized data section
    The program executes knowing that the data is in the RAM
    but the loader puts the initial values in the FLASH (inidata).
    It is one task of the startup to copy the initial values from FLASH to RAM. */
    .data : AT ( _sidata )
    {
        . = ALIGN(4);
        _sdata = .;        	/* create a global symbol at data start; used by startup code in order to initialise the .data section in RAM */
        _ram_start = .;    	/* create a global symbol at ram start for garbage collector */
        . = ALIGN(4);
        *(.data)           	/* .data sections */
        *(.data*)          	/* .data* sections */
        *(.sdata)         	/* .sdata sections */
        *(.sdata*)          /* .sdata* sections */
        . = ALIGN(4);
        _edata = .;        	/* define a global symbol at data end; used by startup code in order to initialise the .data section in RAM */
    } >RAM

    /* Uninitialized data section */
    .bss :
    {
        . = ALIGN(4);
        _sbss = .;         	/* define a global symbol at bss start; used by startup code */
        *(.bss)
        *(.bss*)
        *(.sbss)
        *(.sbss*)
        *(COMMON)

        . = ALIGN(4);
        _ebss = .;         	/* define a global symbol at bss end; used by startup code */
    } >RAM

	/* Check there is RAM left for heap */
	.heap :
    {
        . = ALIGN(4);
        PROVIDE ( end = . );
        _sheap = .;
        . = . + __heap_size;
        . = ALIGN(4);
        _eheap = .;
    } >RAM

	/* Check there is RAM left for stack */
    .stack :
    {
        . = ALIGN(4);
        _estack = .;
        . = . + __stack_size;
        . = ALIGN(4);
        _sstack = .;
    } >RAM
}
