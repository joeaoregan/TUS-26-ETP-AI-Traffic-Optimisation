package com.example.gateway.service;

import com.example.gateway.dto.HealthResponse;
import com.example.gateway.exception.RlInferenceException;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Client for LSTM Traffic Predictor Service. Forecasts edge density for
 * lookahead planning.
 */
@Slf4j
@Service
public class LstmPredictorClient {

	private final RestTemplate restTemplate;

	@Value("${LSTM_PREDICTOR_URL:http://localhost:8001/predict}")
	private String predictorServiceUrl;

	@Value("${lstm.predictor.service.timeout:10000}")
	private int serviceTimeout;

	public LstmPredictorClient(RestTemplate restTemplate) {
		this.restTemplate = restTemplate;
	}

	/**
	 * Get single-step density prediction.
	 *
	 * @param data 3 hourly measurements × 5 edges (shape: 3×5)
	 * @return Predicted densities for 5 edges
	 * @throws RlInferenceException if prediction fails
	 */
	public List<Double> predict(List<List<Double>> data) {
		try {
			log.info("Sending LSTM prediction request to {}", predictorServiceUrl);

			Map<String, Object> requestBody = new HashMap<>();
			requestBody.put("data", data);

			PredictorResponse response = restTemplate.postForObject(predictorServiceUrl, requestBody,
					PredictorResponse.class);

			if (response == null || response.getPrediction() == null) {
				log.error("Received null response from LSTM predictor service");
				throw new RlInferenceException("Received null response from LSTM predictor service");
			}

			log.info("LSTM prediction: {}", response.getPrediction());
			return response.getPrediction();

		} catch (HttpClientErrorException e) {
			log.error("HTTP error from LSTM predictor: {} - {}", e.getStatusCode(), e.getResponseBodyAsString());
			throw new RlInferenceException(String.format("HTTP %d error from LSTM predictor: %s",
					e.getStatusCode().value(), e.getResponseBodyAsString()), e);
		} catch (ResourceAccessException e) {
			log.error("Connection error to LSTM predictor at {}: {}", predictorServiceUrl, e.getMessage());
			throw new RlInferenceException(
					String.format("Failed to connect to LSTM predictor at %s: %s", predictorServiceUrl, e.getMessage()),
					e);
		} catch (Exception e) {
			log.error("Unexpected error during LSTM prediction: {}", e.getMessage(), e);
			throw new RlInferenceException(String.format("Unexpected error during LSTM prediction: %s", e.getMessage()),
					e);
		}
	}

	/**
	 * Get batch predictions for multiple sequences (multi-step ahead).
	 *
	 * @param sequences List of sequences, each 3 timesteps × 5 edges
	 * @return List of predictions, one per input sequence
	 * @throws RlInferenceException if prediction fails
	 */
	public List<List<Double>> predictBatch(List<List<List<Double>>> sequences) {
		try {
			log.info("Sending LSTM batch prediction request ({} sequences) to {}", sequences.size(),
					predictorServiceUrl);

			String batchUrl = predictorServiceUrl.replace("/predict", "/predict-batch");

			Map<String, Object> requestBody = new HashMap<>();
			requestBody.put("sequences", sequences);

			BatchPredictorResponse response = restTemplate.postForObject(batchUrl, requestBody,
					BatchPredictorResponse.class);

			if (response == null || response.getPredictions() == null) {
				log.error("Received null response from LSTM batch predictor service");
				throw new RlInferenceException("Received null response from LSTM batch predictor service");
			}

			log.info("LSTM batch predictions: {} sequences processed", response.getNum_predictions());
			return response.getPredictions();

		} catch (HttpClientErrorException e) {
			log.error("HTTP error from LSTM batch predictor: {} - {}", e.getStatusCode(), e.getResponseBodyAsString());
			throw new RlInferenceException(String.format("HTTP %d error from LSTM batch predictor: %s",
					e.getStatusCode().value(), e.getResponseBodyAsString()), e);
		} catch (ResourceAccessException e) {
			log.error("Connection error to LSTM batch predictor: {}", e.getMessage());
			throw new RlInferenceException(
					String.format("Failed to connect to LSTM batch predictor: %s", e.getMessage()), e);
		} catch (Exception e) {
			log.error("Unexpected error during LSTM batch prediction: {}", e.getMessage(), e);
			throw new RlInferenceException(
					String.format("Unexpected error during LSTM batch prediction: %s", e.getMessage()), e);
		}
	}

	/**
	 * Get model architecture info from the LSTM predictor service.
	 */
	public Map<String, Object> getModelInfo() {
		try {
			String modelInfoUrl = predictorServiceUrl.replace("/predict", "/model-info");
			@SuppressWarnings("unchecked")
			Map<String, Object> response = restTemplate.getForObject(modelInfoUrl, Map.class);
			return response != null ? response : Map.of();
		} catch (Exception e) {
			log.error("Failed to get LSTM model info: {}", e.getMessage());
			throw new RlInferenceException("Failed to get LSTM model info: " + e.getMessage(), e);
		}
	}

	/**
	 * Check health of the LSTM predictor service.
	 *
	 * @return true if service is healthy, false otherwise
	 */
	public boolean isServiceHealthy() {
		try {
			String healthUrl = predictorServiceUrl.replace("/predict", "/health");
			HealthResponse response = restTemplate.getForObject(healthUrl, HealthResponse.class);
			return response != null && "healthy".equals(response.getStatus());
		} catch (Exception e) {
			log.warn("LSTM predictor service health check failed: {}", e.getMessage());
			return false;
		}
	}

	/**
	 * Response DTO for single prediction.
	 */
	@Data
	@NoArgsConstructor
	public static class PredictorResponse {
		private List<Double> prediction;
		private List<String> edge_ids;
		private String timestamp;
		private Double inference_time_ms;
	}

	/**
	 * Response DTO for batch prediction.
	 */
	@Data
	@NoArgsConstructor
	public static class BatchPredictorResponse {
		private List<List<Double>> predictions;
		private List<String> edge_ids;
		private String timestamp;
		private Double inference_time_ms;
		private Integer num_predictions;
	}
}