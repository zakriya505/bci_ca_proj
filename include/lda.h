#ifndef LDA_H
#define LDA_H

#include "types.h"
#include "config.h"

/* LDA Model */
typedef struct {
    signal_t *projection;    /* Projection vector (Fisher's direction) */
    float threshold;         /* Decision threshold */
    size_t num_features;     /* Number of features */
    bool_t is_trained;       /* Training status */
} lda_model_t;

/* Training sample */
typedef struct {
    signal_t *features;      /* Feature vector */
    int label;               /* Class label (0 or 1) */
} lda_sample_t;

/* ========== LDA Functions ========== */

/* Initialize LDA model */
void lda_init(lda_model_t *model, size_t num_features);

/* Train LDA using Fisher's Linear Discriminant */
bool_t lda_train(lda_model_t *model, lda_sample_t *samples, size_t num_samples);

/* Predict class for a feature vector */
int lda_predict(const lda_model_t *model, const signal_t *features);

/* Get projection value */
float lda_project(const lda_model_t *model, const signal_t *features);

/* Free LDA model */
void lda_free(lda_model_t *model);

/* ========== Utility Functions ========== */

/* Calculate accuracy on test set */
float lda_accuracy(const lda_model_t *model, lda_sample_t *samples, size_t num_samples);

#endif /* LDA_H */
