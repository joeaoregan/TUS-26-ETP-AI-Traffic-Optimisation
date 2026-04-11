package com.example.gateway.controller;

import com.example.gateway.dto.ErrorResponse;
import com.example.gateway.dto.HealthResponse;
import com.example.gateway.dto.TrafficActionResponse;
import com.example.gateway.dto.TrafficSignalState;
import com.example.gateway.dto.TrafficForecastResponse;
import com.example.gateway.exception.RlInferenceException;
import com.example.gateway.service.RlInferenceClient;
import com.example.gateway.service.LstmPredictorClient;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.ExampleObject;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.Random;

/**
 * REST Controller for traffic signal control and forecasting.
 * Integrates MAPPO RL inference with LSTM density predictions.
 */
@Slf4j
@RestController
@RequestMapping("/api/traffic")
@RequiredArgsConstructor
public class TrafficController {

	private final RlInferenceClient rlInferenceClient;
	private final LstmPredictorClient lstmPredictorClient;
	private static final Random random = new Random();

	@Value("${rl.inference.observation-dimension:19}")
	private int observationDimension;

	private static final List<String> KNOWN_JUNCTIONS = List.of("joinedS_265580996_300839357", "300839359", "265580972",
			"1270712555", "8541180897");

	/**
	 * Demo endpoint — picks a random junction, generates dummy observations,
	 * returns prediction.
	 */
	@Tag(name = "Traffic Prediction")
	@Operation(operationId = "getTrafficAction", summary = "Get predicted traffic signal action (demo)", description = "Picks a random junction, generates dummy observations and returns the predicted traffic signal state.")
	@SecurityRequirement(name = "bearerAuth")
	@ApiResponse(responseCode = "200", description = "Prediction generated successfully (or Fallback mode if service is down)", content = @Content(mediaType = "application/json", examples = {
			@ExampleObject(name = "Success", summary = "Standard AI Prediction", value = """
					{
					  "junctionId": "300839359",
					  "predictedAction": 1,
					  "signalState": "YELLOW",
					  "timestamp": 1710000000000,
					  "status": "success"
					}
					"""), @ExampleObject(name = "Fallback", summary = "Inference Service Down", value = """
					{
					  "junctionId": "300839359",
					  "predictedAction": 0,
					  "signalState": "RED",
					  "timestamp": 1710000000000,
					  "status": "fallback_mode (inference service down)"
					}
					""") }))
	@ApiResponse(responseCode = "500", description = "Unexpected internal server error", content = @Content(mediaType = "application/json", schema = @Schema(implementation = ErrorResponse.class), examples = @ExampleObject(value = """
			{
			  "status": "error",
			  "message": "Internal server error: null pointer exception",
			  "timestamp": 1710000000000
			}
			""")))
	@GetMapping("/action")
	public ResponseEntity<?> getTrafficAction() {
		String junctionId = KNOWN_JUNCTIONS.get(random.nextInt(KNOWN_JUNCTIONS.size()));
		try {
			log.info("Demo request — using junction={}", junctionId);
			List<Double> observationData = generateDummyObservations(observationDimension);

			int predictedAction = rlInferenceClient.predictAction(junctionId, observationData);
			TrafficSignalState trafficSignalState = mapActionToSignalState(predictedAction);

			TrafficActionResponse response = new TrafficActionResponse(junctionId, predictedAction, trafficSignalState,
					System.currentTimeMillis(), "success");

			log.info("Demo action: junction={} action={} state={}", junctionId, predictedAction, trafficSignalState);
			return ResponseEntity.ok(response);

		} catch (RlInferenceException | org.springframework.web.client.ResourceAccessException e) {
			log.error("Inference service unavailable, entering FALLBACK mode: {}", e.getMessage());

			TrafficActionResponse fallbackResponse = new TrafficActionResponse(junctionId, 0, TrafficSignalState.RED,
					System.currentTimeMillis(), "fallback_mode (inference service down)");

			return ResponseEntity.ok(fallbackResponse);
		}
	}

	/**
	 * Get traffic density forecast for next hour.
	 * Returns predicted densities for 5 monitored edges.
	 */
	@Tag(name = "Traffic Forecasting")
	@Operation(operationId = "getTrafficForecast", summary = "Get traffic density forecast (demo)", description = "Generates dummy historical data (3 hourly measurements) and returns predicted edge densities for next hour.")
	@SecurityRequirement(name = "bearerAuth")
	@ApiResponse(responseCode = "200", description = "Forecast generated successfully", content = @Content(mediaType = "application/json", examples = {
			@ExampleObject(name = "Success", summary = "LSTM Forecast", value = """
					{
					  "edgeIds": ["-269002813", "-55825089", "617128762", "-617128762", "-312266114#2"],
					  "predictedDensities": [22.45, 11.23, 7.89, 5.34, 4.12],
					  "inferenceTimeMs": 28.5,
					  "timestamp": 1710000000000,
					  "status": "success"
					}
					"""), @ExampleObject(name = "Fallback", summary = "LSTM Service Down", value = """
					{
					  "edgeIds": ["-269002813", "-55825089", "617128762", "-617128762", "-312266114#2"],
					  "predictedDensities": [20.0, 10.0, 6.0, 4.0, 3.0],
					  "timestamp": 1710000000000,
					  "status": "fallback_mode"
					}
					""") }))
	@ApiResponse(responseCode = "500", description = "Unexpected internal server error", content = @Content(mediaType = "application/json", schema = @Schema(implementation = ErrorResponse.class)))
	@GetMapping("/forecast")
	public ResponseEntity<?> getTrafficForecast() {
		try {
			log.info("Forecast request — generating dummy historical data");

			// Generate dummy 3 hourly measurements for 5 edges
			List<List<Double>> historicalData = List.of(
					List.of(18.93, 10.13, 5.23, 4.14, 3.08),  // Hour -2
					List.of(24.02, 11.01, 8.98, 5.42, 4.26),  // Hour -1
					List.of(22.14, 9.34, 5.62, 4.57, 3.81)    // Current hour
			);

			long start = System.currentTimeMillis();
			List<Double> prediction = lstmPredictorClient.predict(historicalData);
			double inferenceTimeMs = System.currentTimeMillis() - start;
			String[] edgeIds = { "-269002813", "-55825089", "617128762", "-617128762", "-312266114#2" };

			TrafficForecastResponse response = new TrafficForecastResponse(
					edgeIds,
					prediction.toArray(new Double[0]),
					inferenceTimeMs,
					System.currentTimeMillis(),
					"success",
					null,
					null
			);

			log.info("Forecast generated: edges={} densities={}", edgeIds, prediction);
			return ResponseEntity.ok(response);

		} catch (RlInferenceException | org.springframework.web.client.ResourceAccessException e) {
			log.error("LSTM predictor unavailable, entering FALLBACK mode: {}", e.getMessage());

			// Return fallback forecast with default values
			String[] edgeIds = { "-269002813", "-55825089", "617128762", "-617128762", "-312266114#2" };
			Double[] fallbackDensities = { 20.0, 10.0, 6.0, 4.0, 3.0 };

			TrafficForecastResponse fallbackResponse = new TrafficForecastResponse(
					edgeIds,
					fallbackDensities,
					null,
					System.currentTimeMillis(),
					"fallback_mode (LSTM service unavailable)",
					null,
					e.getMessage()
			);

			return ResponseEntity.ok(fallbackResponse);
		}
	}

	/**
	 * Get multi-step ahead density predictions for lookahead planning.
	 * Accepts custom historical sequences and returns batch predictions.
	 */
	@Tag(name = "Traffic Forecasting")
	@Operation(operationId = "getTrafficForecastBatch", summary = "Get multi-step ahead density predictions", description = "Accepts multiple historical sequences (3 timesteps × 5 edges each) and returns batch predictions for lookahead planning.")
	@SecurityRequirement(name = "bearerAuth")
	@ApiResponse(responseCode = "200", description = "Batch forecast generated successfully", content = @Content(mediaType = "application/json", examples = {
			@ExampleObject(name = "Success", summary = "Batch LSTM Forecast", value = """
					{
					  "edgeIds": ["-269002813", "-55825089", "617128762", "-617128762", "-312266114#2"],
					  "lookaheadPredictions": [
					    [22.45, 11.23, 7.89, 5.34, 4.12],
					    [21.89, 10.95, 7.45, 5.10, 3.95],
					    [20.56, 10.42, 6.89, 4.87, 3.72]
					  ],
					  "inferenceTimeMs": 65.3,
					  "timestamp": 1710000000000,
					  "status": "success"
					}
					""") }))
	@ApiResponse(responseCode = "400", description = "Invalid request format")
	@ApiResponse(responseCode = "500", description = "Unexpected internal server error")
	@PostMapping("/forecast-batch")
	public ResponseEntity<?> getTrafficForecastBatch(@RequestBody BatchForecastRequest request) {
		try {
			log.info("Batch forecast request — {} sequences", request.getSequences().size());

			if (request.getSequences() == null || request.getSequences().isEmpty()) {
				return ResponseEntity.badRequest()
						.body(new ErrorResponse("error", "At least 1 sequence required", System.currentTimeMillis()));
			}

			if (request.getSequences().size() > 100) {
				return ResponseEntity.badRequest()
						.body(new ErrorResponse("error", "Maximum 100 sequences per request", System.currentTimeMillis()));
			}

			long startTime = System.currentTimeMillis();
			List<List<Double>> batchPredictions = lstmPredictorClient.predictBatch(request.getSequences());
			long inferenceTime = System.currentTimeMillis() - startTime;

			String[] edgeIds = { "-269002813", "-55825089", "617128762", "-617128762", "-312266114#2" };

			// Convert to 2D array for response
			Double[][] lookaheadArray = new Double[batchPredictions.size()][];
			for (int i = 0; i < batchPredictions.size(); i++) {
				lookaheadArray[i] = batchPredictions.get(i).toArray(new Double[0]);
			}

			TrafficForecastResponse response = new TrafficForecastResponse(
					edgeIds,
					null,  // No single prediction for batch
					(double) inferenceTime,
					System.currentTimeMillis(),
					"success",
					lookaheadArray,
					null
			);

			log.info("Batch forecast generated: sequences={} lookahead={}", request.getSequences().size(), lookaheadArray.length);
			return ResponseEntity.ok(response);

		} catch (RlInferenceException | org.springframework.web.client.ResourceAccessException e) {
			log.error("LSTM predictor unavailable: {}", e.getMessage());
			return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
					.body(new ErrorResponse("error", "LSTM predictor service unavailable: " + e.getMessage(), System.currentTimeMillis()));
		} catch (Exception e) {
			log.error("Unexpected error during batch forecast: {}", e.getMessage(), e);
			return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
					.body(new ErrorResponse("error", "Internal server error: " + e.getMessage(), System.currentTimeMillis()));
		}
	}

	/**
	 * Predict green phase with real observation data.
	 */
	@Tag(name = "Traffic Prediction")
	@Operation(operationId = "predictTrafficAction", summary = "Predict green phase for a junction",
			description = """
					Accepts real observation values from the junction and returns the predicted green phase index.

					Observation vector layout (observations):
					  [phase_one_hot_0, ..., phase_one_hot_N,   ← current active green phase (one-hot)
					   min_green_flag,                           ← 1 if min green time elapsed, else 0
					   lane_queue_0, lane_queue_1, ...]          ← queue per lane, normalised 0–1

					Sizes: joinedS=19 floats, 300839359≈10 floats, 265580972≈8 floats

					Action (green phase index):
					  joinedS_265580996_300839357: 0–3
					  300839359:                  0–1
					  265580972:                  0–1
					""")
	@SecurityRequirement(name = "bearerAuth")
	@ApiResponse(responseCode = "200", description = "Prediction generated successfully",
			content = @Content(mediaType = "application/json", examples = @ExampleObject(value = """
					{
					  "junctionId": "joinedS_265580996_300839357",
					  "predictedAction": 2,
					  "signalState": "GREEN",
					  "timestamp": 1710000000000,
					  "status": "success"
					}
					""")))
	@ApiResponse(responseCode = "400", description = "Invalid request (missing junctionId or observations)")
	@ApiResponse(responseCode = "503", description = "Inference service unavailable")
	@PostMapping("/action")
	public ResponseEntity<?> predictTrafficAction(
			@io.swagger.v3.oas.annotations.parameters.RequestBody(
					description = "Junction ID and observation vector", required = true,
					content = @Content(mediaType = "application/json", examples = {
							@ExampleObject(name = "joinedS main junction", value = """
									{
									  "junctionId": "joinedS_265580996_300839357",
									  "observations": [0,0,1,0,1,0.2,0.1,0.0,0.3,0.0,0.1,0.0,0.2,0.1,0.0,0.3,0.0,0.1,0.0],
									  "metadata": "morning-peak"
									}
									"""),
							@ExampleObject(name = "300839359 medium junction", value = """
									{
									  "junctionId": "300839359",
									  "observations": [1,0,1,0.3,0.0,0.1,0.2,0.0,0.1,0.0],
									  "metadata": "off-peak"
									}
									"""),
							@ExampleObject(name = "265580972 small junction", value = """
									{
									  "junctionId": "265580972",
									  "observations": [0,1,0,0.1,0.4,0.0,0.2,0.0],
									  "metadata": "off-peak"
									}
									""") }))
			@RequestBody TrafficActionRequest request) {
		try {
			if (request.getJunctionId() == null || request.getJunctionId().isBlank()) {
				return buildErrorResponse("junctionId is required", HttpStatus.BAD_REQUEST);
			}
			if (request.getObservations() == null || request.getObservations().isEmpty()) {
				return buildErrorResponse("observations is required", HttpStatus.BAD_REQUEST);
			}

			log.info("Prediction request: junction={} obs_size={}", request.getJunctionId(), request.getObservations().size());

			int predictedAction = rlInferenceClient.predictAction(request.getJunctionId(), request.getObservations());
			TrafficSignalState signalState = mapActionToSignalState(predictedAction);
			TrafficActionResponse response = new TrafficActionResponse(
					request.getJunctionId(), predictedAction, signalState, System.currentTimeMillis(), "success");

			log.info("Predicted: junction={} action={} state={}", request.getJunctionId(), predictedAction, signalState);
			return ResponseEntity.ok(response);

		} catch (RlInferenceException e) {
			log.error("Inference error: {}", e.getMessage());
			return buildErrorResponse("Inference service error: " + e.getMessage(), HttpStatus.SERVICE_UNAVAILABLE);
		} catch (Exception e) {
			log.error("Unexpected error", e);
			return buildErrorResponse("Internal server error: " + e.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
		}
	}

	/**
	 * Reset MAPPO GRU hidden states for all junctions.
	 */
	@Tag(name = "Traffic Prediction")
	@Operation(operationId = "resetHiddenStates", summary = "Reset MAPPO GRU hidden states",
			description = "Resets the GRU hidden states for all 5 junctions. Call at the start of each new simulation run.")
	@SecurityRequirement(name = "bearerAuth")
	@ApiResponse(responseCode = "200", description = "Hidden states reset successfully")
	@ApiResponse(responseCode = "503", description = "Inference service unavailable")
	@PostMapping("/reset")
	public ResponseEntity<?> resetHiddenStates() {
		try {
			rlInferenceClient.resetHiddenStates();
			return ResponseEntity.ok(Map.of("status", "success", "message", "Hidden states reset for all junctions"));
		} catch (RlInferenceException | org.springframework.web.client.ResourceAccessException e) {
			log.error("Failed to reset hidden states: {}", e.getMessage());
			return buildErrorResponse("Failed to reset hidden states: " + e.getMessage(), HttpStatus.SERVICE_UNAVAILABLE);
		}
	}

	/**
	 * Get combined model info from both RL and LSTM services.
	 */
	@Tag(name = "Traffic Prediction")
	@Operation(operationId = "getModelInfo", summary = "Get model info (RL + LSTM)",
			description = "Returns combined model info from both the MAPPO RL inference service and the LSTM predictor service.")
	@SecurityRequirement(name = "bearerAuth")
	@ApiResponse(responseCode = "200", description = "Model info retrieved — individual service errors reported inline")
	@GetMapping("/model_info")
	public ResponseEntity<?> getModelInfo() {
		Map<String, Object> combined = new java.util.LinkedHashMap<>();

		try {
			combined.put("rl", rlInferenceClient.getModelInfo());
		} catch (Exception e) {
			log.error("Failed to get RL model info: {}", e.getMessage());
			combined.put("rl", Map.of("status", "unavailable", "error", e.getMessage()));
		}

		try {
			combined.put("lstm", lstmPredictorClient.getModelInfo());
		} catch (Exception e) {
			log.error("Failed to get LSTM model info: {}", e.getMessage());
			combined.put("lstm", Map.of("status", "unavailable", "error", e.getMessage()));
		}

		return ResponseEntity.ok(combined);
	}

	/**
	 * Health check — reports status of both RL inference and LSTM predictor services.
	 */
	@Tag(name = "System Health")
	@Operation(operationId = "healthCheck", summary = "Health check",
			description = "Checks both RL inference and LSTM predictor services. Overall status is 'healthy' only if both are up.")
	@ApiResponse(responseCode = "200", description = "All services healthy")
	@ApiResponse(responseCode = "503", description = "One or both services unreachable")
	@GetMapping("/health")
	public ResponseEntity<?> healthCheck() {
		boolean rlHealthy = false;
		boolean lstmHealthy = false;

		try {
			rlHealthy = rlInferenceClient.isServiceHealthy();
		} catch (Exception e) {
			log.warn("RL health check failed: {}", e.getMessage());
		}

		try {
			lstmHealthy = lstmPredictorClient.isServiceHealthy();
		} catch (Exception e) {
			log.warn("LSTM health check failed: {}", e.getMessage());
		}

		String overallStatus = (rlHealthy && lstmHealthy) ? "healthy" : (rlHealthy || lstmHealthy) ? "degraded" : "unhealthy";
		HealthResponse response = new HealthResponse(
				overallStatus,
				rlHealthy ? "up" : "down",
				lstmHealthy ? "up" : "down",
				System.currentTimeMillis());

		HttpStatus httpStatus = rlHealthy && lstmHealthy ? HttpStatus.OK : HttpStatus.SERVICE_UNAVAILABLE;
		return new ResponseEntity<>(response, httpStatus);
	}

	// Helper methods
	private List<Double> generateDummyObservations(int dimension) {
		List<Double> observations = new java.util.ArrayList<>();
		for (int i = 0; i < dimension; i++) {
			observations.add(random.nextDouble());
		}
		return observations;
	}

	private TrafficSignalState mapActionToSignalState(int action) {
		return switch (action) {
			case 0 -> TrafficSignalState.RED;
			case 1 -> TrafficSignalState.YELLOW;
			case 2 -> TrafficSignalState.GREEN;
			case 3 -> TrafficSignalState.GREEN_EXTENDED;
			default -> TrafficSignalState.UNKNOWN;
		};
	}

	private ResponseEntity<ErrorResponse> buildErrorResponse(String message, HttpStatus status) {
		return new ResponseEntity<>(new ErrorResponse("error", message, System.currentTimeMillis()), status);
	}

	/**
	 * Request DTO for traffic signal prediction.
	 */
	@io.swagger.v3.oas.annotations.media.Schema(description = "Request body for traffic signal prediction")
	@lombok.Data
	@lombok.NoArgsConstructor
	@lombok.AllArgsConstructor
	public static class TrafficActionRequest {

		@io.swagger.v3.oas.annotations.media.Schema(description = "Junction ID to predict for",
				example = "joinedS_265580996_300839357",
				allowableValues = { "joinedS_265580996_300839357", "300839359", "265580972",
						"1270712555", "8541180897" })
		private String junctionId;

		@io.swagger.v3.oas.annotations.media.Schema(
				description = "Observation vector: [phase_one_hot..., min_green_flag, lane_queues...]",
				example = "[0,0,1,0,1,0.2,0.1,0.0,0.3,0.0,0.1,0.0,0.2,0.1,0.0,0.3,0.0,0.1,0.0]")
		private List<Double> observations;

		@io.swagger.v3.oas.annotations.media.Schema(description = "Optional metadata for logging",
				example = "morning-peak")
		private String metadata;
	}

	/**
	 * Request DTO for batch forecast endpoint.
	 */
	@lombok.Data
	@lombok.NoArgsConstructor
	@lombok.AllArgsConstructor
	public static class BatchForecastRequest {
		/**
		 * List of sequences, each with 3 timesteps × 5 edges.
		 */
		private List<List<List<Double>>> sequences;
	}
}