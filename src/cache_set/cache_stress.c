/*******************************************************************************
 * Copyright (c) 2017 Dan Iorga, Tyler Sorenson, Alastair Donaldson

 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:

 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.

 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *******************************************************************************/

 /**
  * @file cache_stress.c
  * @author Dan Iorga, Tyler Sorenson, Alastair Donaldson
  * @date 1 Nov 2017
  * @brief Run through the cache
  *
  * This test runs through a region of memory the size of the
  * L3 cache, striding at the size of a cache line (64 bytes)
  * Makes lots of accesses to the l3. Hopefully sensative to stress
  * on that cache
  */

#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/resource.h>

#include "../common/common.h"

/** Helper defines for cache allocation */
#define KB              ((1) << 10)

/** The size of the cache */
#define CACHE_SIZE      SIZE * KB

/** Wrap the code in a loop consisting of ITERATIONS iterations */
#define ITERATIONS      500

/**
 @brief this main func
 @ return 0 on success
 */
int main(int argc, char *argv[]) {

    register volatile int * my_array;
    register unsigned int sum = 0;
    long begin = 0;
    long end = 0;
    float amplifier;
    long size = CACHE_SIZE;

    struct rusage usage_start, usage_stop;

    if (argc==2) {
            amplifier = atof(argv[1]);
            size = (int) amplifier * CACHE_SIZE;
    }


    my_array = (int *) malloc(size);
    DIE(my_array == NULL, "Unable to allocate memory");

    for (int i = 0; i < size/sizeof(int); i++) my_array[i] = i;

    getrusage(RUSAGE_SELF, &usage_start);
    begin = get_current_time_us();


#ifdef INFINITE
    while(1) {
#else
    for (int it = 0; it < ITERATIONS; it++) {
#endif
        for (int i = 0; i < size/sizeof(int); i+=CACHE_LINE/4) {
                sum += my_array[i];
            }
    }


    end = get_current_time_us();
    getrusage(RUSAGE_SELF, &usage_stop);

    printf("Voluntary_switches %ld\n", usage_stop.ru_nvcsw - usage_start.ru_nvcsw);
    printf("Involuntary_switches %ld\n", usage_stop.ru_nivcsw - usage_start.ru_nivcsw);

    printf("Sum: %u\n", sum);
    printf("total time(us): %ld\n", end - begin);

    free( (void *) my_array);
    return 0;
}
