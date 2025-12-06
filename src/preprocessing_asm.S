# RISC-V Assembly Optimized Functions
# Moving Average Filter Implementation
# Target: RISC-V 32-bit architecture

.section .text
.globl moving_average_asm

# Function: moving_average_asm
# Purpose: Compute moving average filter optimized for RISC-V
# Arguments:
#   a0 = const float *input (input signal array)
#   a1 = float *output (output signal array)
#   a2 = size_t length (array length)
#   a3 = size_t window (window size)
# Returns: void

moving_average_asm:
    # Save callee-saved registers
    addi sp, sp, -32
    sw s0, 0(sp)
    sw s1, 4(sp)
    sw s2, 8(sp)
    sw s3, 12(sp)
    sw s4, 16(sp)
    sw s5, 20(sp)
    sw ra, 24(sp)
    
    # Initialize loop variables
    li s0, 0                # i = 0 (outer loop counter)
    mv s1, a2               # s1 = length
    mv s2, a3               # s2 = window size
    mv s3, a0               # s3 = input pointer
    mv s4, a1               # s4 = output pointer
    
outer_loop:
    bge s0, s1, end_outer   # if i >= length, exit
    
    # Initialize sum and count for this window
    li t0, 0                # count = 0
    fcvt.s.w f0, zero       # sum = 0.0 (float)
    
    # Inner loop: calculate sum over window
    li s5, 0                # j = 0
    
inner_loop:
    bge s5, s2, end_inner   # if j >= window, exit inner loop
    
    # Check if i >= j (valid index)
    sub t1, s0, s5          # t1 = i - j
    bltz t1, skip_sample    # if i < j, skip
    
    # Load input[i-j]
    slli t2, t1, 2          # t2 = (i-j) * 4 (float size)
    add t3, s3, t2          # t3 = &input[i-j]
    flw f1, 0(t3)           # f1 = input[i-j]
    
    # Add to sum
    fadd.s f0, f0, f1       # sum += input[i-j]
    addi t0, t0, 1          # count++
    
skip_sample:
    addi s5, s5, 1          # j++
    j inner_loop
    
end_inner:
    # Calculate average: sum / count
    fcvt.s.w f2, t0         # f2 = (float)count
    fdiv.s f3, f0, f2       # f3 = sum / count
    
    # Store result: output[i] = average
    slli t4, s0, 2          # t4 = i * 4
    add t5, s4, t4          # t5 = &output[i]
    fsw f3, 0(t5)           # output[i] = average
    
    # Increment outer loop counter
    addi s0, s0, 1          # i++
    j outer_loop
    
end_outer:
    # Restore callee-saved registers
    lw s0, 0(sp)
    lw s1, 4(sp)
    lw s2, 8(sp)
    lw s3, 12(sp)
    lw s4, 16(sp)
    lw s5, 20(sp)
    lw ra, 24(sp)
    addi sp, sp, 32
    
    ret
