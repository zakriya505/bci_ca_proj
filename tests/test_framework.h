#ifndef TEST_FRAMEWORK_H
#define TEST_FRAMEWORK_H

#include <stdio.h>
#include <math.h>

/* Simple test framework */
static int tests_run = 0;
static int tests_passed = 0;
static int tests_failed = 0;

#define ASSERT_TRUE(condition, message) do { \
    tests_run++; \
    if (condition) { \
        tests_passed++; \
        printf("  ✓ PASS: %s\n", message); \
    } else { \
        tests_failed++; \
        printf("  ✗ FAIL: %s\n", message); \
    } \
} while(0)

#define ASSERT_EQUAL(expected, actual, message) do { \
    tests_run++; \
    if ((expected) == (actual)) { \
        tests_passed++; \
        printf("  ✓ PASS: %s (expected: %d, got: %d)\n", message, expected, actual); \
    } else { \
        tests_failed++; \
        printf("  ✗ FAIL: %s (expected: %d, got: %d)\n", message, expected, actual); \
    } \
} while(0)

#define ASSERT_FLOAT_EQUAL(expected, actual, tolerance, message) do { \
    tests_run++; \
    float diff = fabsf((expected) - (actual)); \
    if (diff < (tolerance)) { \
        tests_passed++; \
        printf("  ✓ PASS: %s (expected: %.4f, got: %.4f, diff: %.6f)\n", \
               message, (float)(expected), (float)(actual), diff); \
    } else { \
        tests_failed++; \
        printf("  ✗ FAIL: %s (expected: %.4f, got: %.4f, diff: %.6f)\n", \
               message, (float)(expected), (float)(actual), diff); \
    } \
} while(0)

#define TEST_SUITE_START(name) do { \
    printf("\n╔════════════════════════════════════════════════════════════════╗\n"); \
    printf("║ Test Suite: %-50s ║\n", name); \
    printf("╚════════════════════════════════════════════════════════════════╝\n\n"); \
} while(0)

#define TEST_START(name) do { \
    printf("\n[TEST] %s\n", name); \
} while(0)

#define TEST_SUITE_END() do { \
    printf("\n════════════════════════════════════════════════════════════════\n"); \
    printf("Test Results:\n"); \
    printf("  Total:  %d\n", tests_run); \
    printf("  Passed: %d (%.1f%%)\n", tests_passed, \
           tests_run > 0 ? (100.0f * tests_passed / tests_run) : 0.0f); \
    printf("  Failed: %d\n", tests_failed); \
    printf("════════════════════════════════════════════════════════════════\n\n"); \
} while(0)

#endif /* TEST_FRAMEWORK_H */
