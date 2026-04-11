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

			List<Double> prediction = lstmPredictorClient.predict(historicalData);
			String[] edgeIds = { "-269002813", "-55825089", "617128762", "-617128762", "-312266114#2" };

			TrafficForecastResponse response = new TrafficForecastResponse(
					edgeIds,
					prediction.toArray(new Double[0]),
					null,  // Will be set by client
					System.currentTimeMillis(),
					"success",
					null,  // No lookahead for single prediction
					null   // No error
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
			default -> TrafficSignalState.RED;
		};
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