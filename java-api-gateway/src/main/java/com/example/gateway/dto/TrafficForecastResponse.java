package com.example.gateway.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Response DTO for traffic density forecast endpoint.
 * Returns predicted edge densities for lookahead planning.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class TrafficForecastResponse {

    /**
     * Edge IDs for the 5 monitored edges.
     */
    private String[] edgeIds;

    /**
     * Predicted densities for each edge (next hour).
     */
    private Double[] predictedDensities;

    /**
     * Inference latency in milliseconds.
     */
    private Double inferenceTimeMs;

    /**
     * Timestamp of prediction generation.
     */
    private Long timestamp;

    /**
     * Service status: "success" or "fallback_mode"
     */
    private String status;

    /**
     * Optional: Multi-step ahead predictions for lookahead.
     * List of predictions for next 3 hours (if batch request).
     */
    private Double[][] lookaheadPredictions;

    /**
     * Error message if status is "error"
     */
    private String errorMessage;
}