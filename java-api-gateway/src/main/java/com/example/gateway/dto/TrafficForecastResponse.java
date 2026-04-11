package com.example.gateway.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Response DTO for traffic density forecast endpoint. Returns predicted edge
 * densities for lookahead planning.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
@Schema(description = "Traffic density forecast response with predictions for monitored edges")
public class TrafficForecastResponse {

	/**
	 * Edge IDs for the 5 monitored edges.
	 */
	@Schema(description = "Array of edge IDs", example = "[\"-269002813\", \"-55825089\", \"617128762\", \"-617128762\", \"-312266114#2\"]")
	private String[] edgeIds;

	/**
	 * Predicted densities for each edge (next hour).
	 */
	@Schema(description = "Predicted vehicle densities for each edge", example = "[32.20, 5.65, 10.34, 6.49, 11.16]")
	private Double[] predictedDensities;

	/**
	 * Inference latency in milliseconds.
	 */
	@Schema(description = "Inference execution time in milliseconds", example = "28.5")
	private Double inferenceTimeMs;

	/**
	 * Timestamp of prediction generation.
	 */
	@Schema(description = "Unix timestamp when prediction was generated", example = "1775902906572")
	private Long timestamp;

	/**
	 * Service status: "success" or "fallback_mode"
	 */
	@Schema(description = "Request status", example = "success", allowableValues = { "success", "fallback_mode",
			"error" })
	private String status;

	/**
	 * Optional: Multi-step ahead predictions for lookahead. List of predictions for
	 * next 3 hours (if batch request).
	 */
	@Schema(description = "Multi-step ahead predictions for lookahead planning (batch requests only)", example = "[[32.20, 5.65, 10.34, 6.49, 11.16], [31.89, 5.50, 10.10, 6.25, 10.95]]")
	private Double[][] lookaheadPredictions;

	/**
	 * Error message if status is "error"
	 */
	@Schema(description = "Error message (populated when status is 'error')", example = "LSTM predictor service unavailable")
	private String errorMessage;
}