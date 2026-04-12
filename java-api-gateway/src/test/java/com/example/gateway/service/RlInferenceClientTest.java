package com.example.gateway.service;

import com.example.gateway.exception.RlInferenceException;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class RlInferenceClientTest {

	@Mock
	private RestTemplate restTemplate;

	@InjectMocks
	private RlInferenceClient rlInferenceClient;

	@Test
	@DisplayName("predictAction returns action from inference service")
	void predictAction_success() {
		ReflectionTestUtils.setField(rlInferenceClient, "inferenceServiceUrl", "http://localhost:8000/predict_action");

		var response = new RlInferenceClient.PredictionResponse();
		response.setAction(2);
		response.setConfidence(0.87);

		when(restTemplate.postForObject(anyString(), any(), eq(RlInferenceClient.PredictionResponse.class)))
				.thenReturn(response);

		int action = rlInferenceClient.predictAction("300839359", List.of(0.1, 0.2, 0.3));
		assertEquals(2, action);
	}

	@Test
	@DisplayName("predictAction throws RlInferenceException on null response")
	void predictAction_nullResponse() {
		ReflectionTestUtils.setField(rlInferenceClient, "inferenceServiceUrl", "http://localhost:8000/predict_action");

		when(restTemplate.postForObject(anyString(), any(), eq(RlInferenceClient.PredictionResponse.class)))
				.thenReturn(null);

		assertThrows(RlInferenceException.class,
				() -> rlInferenceClient.predictAction("300839359", List.of(0.1)));
	}

	@Test
	@DisplayName("predictAction throws RlInferenceException on connection failure")
	void predictAction_connectionFailure() {
		ReflectionTestUtils.setField(rlInferenceClient, "inferenceServiceUrl", "http://localhost:8000/predict_action");

		when(restTemplate.postForObject(anyString(), any(), eq(RlInferenceClient.PredictionResponse.class)))
				.thenThrow(new ResourceAccessException("Connection refused"));

		assertThrows(RlInferenceException.class,
				() -> rlInferenceClient.predictAction("300839359", List.of(0.1)));
	}

	@Test
	@DisplayName("isServiceHealthy returns true when service responds healthy")
	void isServiceHealthy_true() {
		ReflectionTestUtils.setField(rlInferenceClient, "inferenceServiceUrl", "http://localhost:8000/predict_action");

		var health = new RlInferenceClient.HealthResponse();
		health.setStatus("healthy");
		health.setModelLoaded(true);

		when(restTemplate.getForObject(anyString(), eq(RlInferenceClient.HealthResponse.class)))
				.thenReturn(health);

		assertTrue(rlInferenceClient.isServiceHealthy());
	}

	@Test
	@DisplayName("isServiceHealthy returns false when service is down")
	void isServiceHealthy_false() {
		ReflectionTestUtils.setField(rlInferenceClient, "inferenceServiceUrl", "http://localhost:8000/predict_action");

		when(restTemplate.getForObject(anyString(), eq(RlInferenceClient.HealthResponse.class)))
				.thenThrow(new ResourceAccessException("Connection refused"));

		assertFalse(rlInferenceClient.isServiceHealthy());
	}
}
