# RISC-V Assembly Optimized Functions
# Feature Extraction Implementation
# Target: RISC-V 32-bit architecture

.section .text
.globl calculate_power_asm
.globl calculate_variance_asm

# Function: calculate_power_asm
# Purpose: Calculate signal power (sum of squares) optimized for RISC-V
# Arguments:
#   a0 = const float *signal (signal array)
#   a1 = size_t length (array length)
# Returns: float (in fa0)

calculate_power_asm:
    # Save callee-saved registers
    addi sp, sp, -16
    sw s0, 0(sp)
    sw s1, 4(sp)
    sw ra, 8(sp)
    
    # Initialize
    li s0, 0                # i = 0
    mv s1, a1               # s1 = length
    fcvt.s.w f0, zero       # power = 0.0
    
power_loop:
    bge s0, s1, end_power   # if i >= length, exit
    
    # Load signal[i]
    slli t0, s0, 2          # t0 = i * 4
    add t1, a0, t0          # t1 = &signal[i]
    flw f1, 0(t1)           # f1 = signal[i]
    
    # Square the value: signal[i] * signal[i]
    fmul.s f2, f1, f1       # f2 = signal[i]^2
    
    # Add to power
    fadd.s f0, f0, f2       # power += signal[i]^2
    
    # Increment counter
    addi s0, s0, 1          # i++
    j power_loop
    
end_power:
    # Normalize by length: power / length
    fcvt.s.w f3, s1         # f3 = (float)length
    fdiv.s f0, f0, f3       # power /= length
    
    # Result is in f0, move to fa0 for return
    fmv.s fa0, f0
    
    # Restore registers
    lw s0, 0(sp)
    lw s1, 4(sp)
    lw ra, 8(sp)
    addi sp, sp, 16
    
    ret


# Function: calculate_variance_asm
# Purpose: Calculate signal variance optimized for RISC-V
# Arguments:
#   a0 = const float *signal (signal array)
#   a1 = size_t length (array length)
#   fa0 = float mean (mean value)
# Returns: float (in fa0)

calculate_variance_asm:
    # Save callee-saved registers
    addi sp, sp, -16
    sw s0, 0(sp)
    sw s1, 4(sp)
    sw ra, 8(sp)
    
    # Save mean in f10
    fmv.s f10, fa0
    
    # Initialize
    li s0, 0                # i = 0
    mv s1, a1               # s1 = length
    fcvt.s.w f0, zero       # variance = 0.0
    
variance_loop:
    bge s0, s1, end_variance # if i >= length, exit
    
    # Load signal[i]
    slli t0, s0, 2          # t0 = i * 4
    add t1, a0, t0          # t1 = &signal[i]
    flw f1, 0(t1)           # f1 = signal[i]
    
    # Calculate diff = signal[i] - mean
    fsub.s f2, f1, f10      # f2 = signal[i] - mean
    
    # Square the difference
    fmul.s f3, f2, f2       # f3 = diff^2
    
    # Add to variance
    fadd.s f0, f0, f3       # variance += diff^2
    
    # Increment counter
    addi s0, s0, 1          # i++
    j variance_loop
    
end_variance:
    # Normalize by length: variance / length
    fcvt.s.w f4, s1         # f4 = (float)length
    fdiv.s f0, f0, f4       # variance /= length
    
    # Result is in f0, move to fa0 for return
    fmv.s fa0, f0
    
    # Restore registers
    lw s0, 0(sp)
    lw s1, 4(sp)
    lw ra, 8(sp)
    addi sp, sp, 16
    
    ret
