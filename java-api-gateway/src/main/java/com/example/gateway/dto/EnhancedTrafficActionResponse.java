package com.example.gateway.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * Response combining LSTM forecast with RL signal prediction.
 * Demonstrates the proactive control pipeline: LSTM predicts future density,
 * which informs the RL agent's signal decision.
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
@Schema(description = "Enhanced response combining LSTM density forecast with RL signal prediction")
public class EnhancedTrafficActionResponse {

	@Schema(description = "Junction ID", example = "300839359")
	private String junctionId;

	@Schema(description = "Predicted action index from RL model", example = "2")
	private int predictedAction;

	@Schema(description = "Human-readable signal state", example = "GREEN")
	private TrafficSignalState signalState;

	@Schema(description = "Predicted edge densities for next hour (from LSTM)", example = "[22.45, 11.23, 7.89, 5.34, 4.12]")
	private Double[] forecastedDensities;

	@Schema(description = "Whether LSTM forecast was used to augment the RL observation", example = "true")
	private boolean forecastAugmented;

	@Schema(description = "RL model confidence in the selected action", example = "0.87")
	private Double confidence;

	@Schema(description = "Total pipeline latency in ms (LSTM + RL)", example = "45.2")
	private Double pipelineLatencyMs;

	@Schema(description = "Unix timestamp", example = "1710000000000")
	private long timestamp;

	@Schema(description = "Status", example = "success")
	private String status;
}
