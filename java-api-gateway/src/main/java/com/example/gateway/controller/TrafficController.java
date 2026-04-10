package com.example.gateway.controller;

import com.example.gateway.dto.ErrorResponse;
import com.example.gateway.dto.HealthResponse;
import com.example.gateway.dto.TrafficActionResponse;
import com.example.gateway.dto.TrafficSignalState;
import com.example.gateway.exception.RlInferenceException;
import com.example.gateway.service.RlInferenceClient;

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
 * REST Controller for traffic signal control via MAPPO inference.
 */
@Slf4j
@RestController
@RequestMapping("/api/traffic")
@RequiredArgsConstructor
public class TrafficController {

	private final RlInferenceClient rlInferenceClient;
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
	 * Predict traffic action for a specific junction with provided observations.
	 */
	@Tag(name = "Traffic Prediction")
	@Operation(operationId = "predictTrafficAction", summary = "Predict traffic signal action for a junction", description = "Accepts a junction ID and its local observation vector, returns the MAPPO model prediction.")
	@SecurityRequirement(name = "bearerAuth")
	@ApiResponse(responseCode = "200", description = "Prediction generated successfully", content = @Content(mediaType = "application/json", schema = @Schema(oneOf = {
			TrafficActionResponse.class }), examples = { @ExampleObject(name = "Success", value = """
					{
					  "junctionId": "joinedS_265580996_300839357",
					  "predictedAction": 2,
					  "signalState": "GREEN",
					  "timestamp": 1710000000000,
					  "status": "success"
					}
					"""), @ExampleObject(name = "Fallback (Inference Down)", value = """
					{
					  "junctionId": "300839359",
					  "predictedAction": 0,
					  "signalState": "RED",
					  "timestamp": 1710000000000,
					  "status": "fallback_mode (inference service down)"
					}
					""") }))
	@ApiResponse(responseCode = "400", description = "Invalid request body", content = @Content(mediaType = "application/json", schema = @Schema(implementation = ErrorResponse.class), examples = @ExampleObject(value = """
			{
			  "status": "error",
			  "message": "junctionId is required",
			  "timestamp": 1710000000000
			}
			""")))
	@ApiResponse(responseCode = "401", description = "Unauthorized - invalid or missing JWT")
	@ApiResponse(responseCode = "500", description = "Unexpected internal server error", content = @Content(mediaType = "application/json", schema = @Schema(implementation = ErrorResponse.class), examples = @ExampleObject(value = """
			{
			  "status": "error",
			  "message": "Internal server error: unexpected exception",
			  "timestamp": 1710000000000
			}
			""")))
	@PostMapping("/action")
	public ResponseEntity<?> predictTrafficAction(
			@io.swagger.v3.oas.annotations.parameters.RequestBody(description = "Junction ID and observation vector", required = true, content = @Content(mediaType = "application/json", examples = {
					@ExampleObject(name = "joinedS junction (19 obs)", value = """
							{
							  "junctionId": "joinedS_265580996_300839357",
							  "observations": [0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.12,
							                   0.08, 0.33, 0.41, 0.22, 0.55, 0.18, 0.62, 0.70, 0.81, 0.50],
							  "metadata": "morning-peak"
							}
							"""), @ExampleObject(name = "2-phase junction (8 obs)", value = """
							{
							  "junctionId": "300839359",
							  "observations": [0.0, 1.0, 1.0, 0.12, 0.33, 0.41, 0.22, 0.55],
							  "metadata": "off-peak"
							}
							""") })) @RequestBody TrafficActionRequest request) {
		try {
			if (request.getJunctionId() == null || request.getJunctionId().isBlank()) {
				return buildErrorResponse("junctionId is required", HttpStatus.BAD_REQUEST);
			}

			if (request.getObservations() == null || request.getObservations().isEmpty()) {
				return buildErrorResponse("observations is required", HttpStatus.BAD_REQUEST);
			}

			if (request.getObservations().size() > observationDimension) {
				return buildErrorResponse(String.format("observations exceeds max size of %d (received %d)",
						observationDimension, request.getObservations().size()), HttpStatus.BAD_REQUEST);
			}

			log.info("Prediction request: junction={} obs_size={}", request.getJunctionId(),
					request.getObservations().size());

			int predictedAction = rlInferenceClient.predictAction(request.getJunctionId(), request.getObservations());
			TrafficSignalState trafficSignalState = mapActionToSignalState(predictedAction);

			TrafficActionResponse response = new TrafficActionResponse(request.getJunctionId(), predictedAction,
					trafficSignalState, System.currentTimeMillis(), "success");

			log.info("Prediction: junction={} action={} state={}", request.getJunctionId(), predictedAction,
					trafficSignalState);
			return ResponseEntity.ok(response);

		} catch (RlInferenceException | org.springframework.web.client.ResourceAccessException e) {
			log.error("Inference service unavailable, entering FALLBACK mode: {}", e.getMessage());

			TrafficActionResponse response = new TrafficActionResponse(request.getJunctionId(), 0,
					TrafficSignalState.RED, System.currentTimeMillis(), "fallback_mode (inference service down)");

			return ResponseEntity.ok(response);

		} catch (Exception e) {
			log.error("Unexpected error", e);
			return buildErrorResponse("Internal server error: " + e.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
		}
	}

	/**
	 * Reset GRU hidden states on the inference service. Call at the start of each
	 * new simulation run.
	 */
	@Tag(name = "Traffic Prediction")
	@Operation(operationId = "resetHiddenStates", summary = "Reset MAPPO hidden states", description = "Resets GRU hidden states for all junctions. Call at the start of each new simulation run.")
	@SecurityRequirement(name = "bearerAuth")
	@ApiResponse(responseCode = "200", description = "Hidden states reset successfully", content = @Content(mediaType = "application/json", examples = @ExampleObject(value = """
			{
			  "status": "ok",
			  "message": "Hidden states reset for all junctions"
			}
			""")))
	@PostMapping("/reset")
	public ResponseEntity<?> resetHiddenStates() {
		try {
			rlInferenceClient.resetHiddenStates();
			return ResponseEntity
					.ok(java.util.Map.of("status", "ok", "message", "Hidden states reset for all junctions"));
		} catch (RlInferenceException e) {
			log.error("Failed to reset hidden states: {}", e.getMessage());
			return buildErrorResponse("Failed to reset hidden states: " + e.getMessage(),
					HttpStatus.SERVICE_UNAVAILABLE);
		}
	}

	/**
	 * Get MAPPO model info from the inference service.
	 */
	@Tag(name = "Traffic Prediction")
	@Operation(operationId = "getModelInfo", summary = "Get MAPPO model info",
		description = "Returns architecture details and junction configuration of the loaded MAPPO model.")
	@SecurityRequirement(name = "bearerAuth")
	@GetMapping("/model_info")
	public ResponseEntity<?> getModelInfo() {
		try {
			Map<String, Object> response = rlInferenceClient.getModelInfo();
			return ResponseEntity.ok(response);
		} catch (RlInferenceException e) {
			log.error("Model info failed: {}", e.getMessage());
			return buildErrorResponse("Failed to get model info: " + e.getMessage(),
					HttpStatus.SERVICE_UNAVAILABLE);
		}
	}

	/**
	 * Health check endpoint.
	 */
	@Tag(name = "System Health")
	@Operation(operationId = "healthCheck", summary = "Health check", description = "Checks whether the RL inference service is reachable and responding.")
	@ApiResponse(responseCode = "200", description = "Service is healthy", content = @Content(mediaType = "application/json", schema = @Schema(implementation = HealthResponse.class), examples = {
			@ExampleObject(name = "Healthy", value = """
					{
					  "status": "healthy",
					  "inferenceService": "up",
					  "timestamp": 1710000000000
					}
					"""), @ExampleObject(name = "Degraded", value = """
					{
					  "status": "degraded",
					  "inferenceService": "down",
					  "timestamp": 1774149764299
					}
					""") }))
	@ApiResponse(responseCode = "500", description = "Health check failed", content = @Content(mediaType = "application/json", schema = @Schema(implementation = ErrorResponse.class), examples = @ExampleObject(value = """
			{
			  "status": "unhealthy",
			  "inferenceService": "down",
			  "timestamp": 1710000000000
			}
			""")))
	@GetMapping("/health")
	public ResponseEntity<?> healthCheck() {
		try {
			boolean inferenceServiceHealthy = rlInferenceClient.isServiceHealthy();

			HealthResponse response = new HealthResponse(inferenceServiceHealthy ? "healthy" : "degraded",
					inferenceServiceHealthy ? "up" : "down", System.currentTimeMillis());

			HttpStatus status = inferenceServiceHealthy ? HttpStatus.OK : HttpStatus.SERVICE_UNAVAILABLE;
			return new ResponseEntity<>(response, status);

		} catch (Exception e) {
			log.warn("Health check failed: {}", e.getMessage());
			return new ResponseEntity<>(new HealthResponse("unhealthy", "down", System.currentTimeMillis()),
					HttpStatus.INTERNAL_SERVER_ERROR);
		}
	}

	private List<Double> generateDummyObservations(int size) {
		List<Double> observations = new java.util.ArrayList<>();
		for (int i = 0; i < size; i++) {
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
	 * Request model for traffic action prediction.
	 */
	@Schema(description = "Request body for traffic signal action prediction")
	@lombok.Data
	@lombok.NoArgsConstructor
	@lombok.AllArgsConstructor
	public static class TrafficActionRequest {

		@Schema(description = "Junction ID to predict for", example = "300839359", requiredMode = Schema.RequiredMode.REQUIRED)
		private String junctionId;

		@Schema(description = "Local observation vector (up to 19 floats). Smaller obs are zero-padded internally.", example = "[0.0, 1.0, 1.0, 0.12, 0.33, 0.41, 0.22, 0.55]")
		private List<Double> observations;

		@Schema(description = "Optional metadata for debugging or tracking", example = "peak-hour")
		private String metadata;
	}
}
