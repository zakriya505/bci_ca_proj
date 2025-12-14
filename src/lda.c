#include "lda.h"
#include "utils.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>

/* ========== LDA Initialization ========== */

void lda_init(lda_model_t *model, size_t num_features) {
    model->num_features = num_features;
    model->threshold = 0.0f;
    model->is_trained = FALSE;
    
    /* Allocate projection vector */
    model->projection = (signal_t*)calloc(num_features, sizeof(signal_t));
    
    if (model->projection == NULL) {
        log_error("Failed to allocate LDA projection vector");
    }
}

/* ========== Helper Functions ========== */

static void compute_mean(lda_sample_t *samples, size_t num_samples, 
                        int target_label, signal_t *mean, size_t num_features) {
    /* Initialize mean to zero */
    for (size_t i = 0; i < num_features; i++) {
        mean[i] = 0.0f;
    }
    
    /* Sum features for target class */
    size_t count = 0;
    for (size_t i = 0; i < num_samples; i++) {
        if (samples[i].label == target_label) {
            for (size_t j = 0; j < num_features; j++) {
                mean[j] += samples[i].features[j];
            }
            count++;
        }
    }
    
    /* Divide by count */
    if (count > 0) {
        for (size_t i = 0; i < num_features; i++) {
            mean[i] /= count;
        }
    }
}

static float compute_within_class_variance(lda_sample_t *samples, size_t num_samples,
                                          const signal_t *mean, size_t num_features) {
    float variance = 0.0f;
    size_t count = 0;
    
    for (size_t i = 0; i < num_samples; i++) {
        for (size_t j = 0; j < num_features; j++) {
            float diff = samples[i].features[j] - mean[j];
            variance += diff * diff;
        }
        count++;
    }
    
    return (count > 0) ? (variance / count) : 1.0f;
}

/* ========== LDA Training (Fisher's Linear Discriminant) ========== */

bool_t lda_train(lda_model_t *model, lda_sample_t *samples, size_t num_samples) {
    if (model == NULL || samples == NULL || num_samples == 0) {
        return FALSE;
    }
    
    size_t n = model->num_features;
    
    /* Allocate temporary arrays */
    signal_t *mean0 = (signal_t*)malloc(n * sizeof(signal_t));
    signal_t *mean1 = (signal_t*)malloc(n * sizeof(signal_t));
    
    if (mean0 == NULL || mean1 == NULL) {
        free(mean0);
        free(mean1);
        return FALSE;
    }
    
    /* Compute mean vectors for each class */
    compute_mean(samples, num_samples, 0, mean0, n);
    compute_mean(samples, num_samples, 1, mean1, n);
    
    /* Fisher's LDA: w = (mean1 - mean0) / (variance0 + variance1) */
    /* Simplified version: w ∝ (mean1 - mean0) */
    
    /* Calculate mean difference */
    float norm = 0.0f;
    for (size_t i = 0; i < n; i++) {
        model->projection[i] = mean1[i] - mean0[i];
        norm += model->projection[i] * model->projection[i];
    }
    
    /* Normalize projection vector */
    norm = sqrtf(norm);
    if (norm > 0.0001f) {
        for (size_t i = 0; i < n; i++) {
            model->projection[i] /= norm;
        }
    }
    
    /* Calculate threshold as midpoint between projected means */
    float projected_mean0 = 0.0f,projected_mean1 = 0.0f;
    for (size_t i = 0; i < n; i++) {
        projected_mean0 += model->projection[i] * mean0[i];
        projected_mean1 += model->projection[i] * mean1[i];
    }
    model->threshold = (projected_mean0 + projected_mean1) / 2.0f;
    
    /* Cleanup */
    free(mean0);
    free(mean1);
    
    model->is_trained = TRUE;
    return TRUE;
}

/* ========== LDA Prediction ========== */

float lda_project(const lda_model_t *model, const signal_t *features) {
    if (!model->is_trained) {
        return 0.0f;
    }
    
    float projection = 0.0f;
    for (size_t i = 0; i < model->num_features; i++) {
        projection += model->projection[i] * features[i];
    }
    
    return projection;
}

int lda_predict(const lda_model_t *model, const signal_t *features) {
    float projection = lda_project(model, features);
    return (projection >= model->threshold) ? 1 : 0;
}

/* ========== Utility Functions ========== */

float lda_accuracy(const lda_model_t *model, lda_sample_t *samples, size_t num_samples) {
    if (num_samples == 0) {
        return 0.0f;
    }
    
    size_t correct = 0;
    for (size_t i = 0; i < num_samples; i++) {
        int prediction = lda_predict(model, samples[i].features);
        if (prediction == samples[i].label) {
            correct++;
        }
    }
    
    return (float)correct / num_samples;
}

void lda_free(lda_model_t *model) {
    if (model != NULL && model->projection != NULL) {
        free(model->projection);
        model->projection = NULL;
        model->is_trained = FALSE;
    }
}
