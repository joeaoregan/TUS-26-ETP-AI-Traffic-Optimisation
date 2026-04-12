package com.example.gateway.controller;

import com.example.gateway.dto.TrafficActionResponse;
import com.example.gateway.dto.TrafficSignalState;
import com.example.gateway.exception.RlInferenceException;
import com.example.gateway.service.LstmPredictorClient;
import com.example.gateway.service.RlInferenceClient;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;

import java.util.List;

import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class TrafficControllerTest {

	@Autowired
	private MockMvc mockMvc;

	@MockBean
	private RlInferenceClient rlInferenceClient;

	@MockBean
	private LstmPredictorClient lstmPredictorClient;

	@Test
	@WithMockUser
	@DisplayName("GET /api/traffic/action returns prediction when RL service is healthy")
	void getTrafficAction_success() throws Exception {
		when(rlInferenceClient.predictAction(anyString(), anyList())).thenReturn(2);

		mockMvc.perform(get("/api/traffic/action"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.predictedAction").value(2))
				.andExpect(jsonPath("$.signalState").value("GREEN"))
				.andExpect(jsonPath("$.status").value("success"));
	}

	@Test
	@WithMockUser
	@DisplayName("GET /api/traffic/action returns RED fallback when RL service is down")
	void getTrafficAction_fallback() throws Exception {
		when(rlInferenceClient.predictAction(anyString(), anyList()))
				.thenThrow(new RlInferenceException("Connection refused"));

		mockMvc.perform(get("/api/traffic/action"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.predictedAction").value(0))
				.andExpect(jsonPath("$.signalState").value("RED"))
				.andExpect(jsonPath("$.status").value(org.hamcrest.Matchers.containsString("fallback")));
	}

	@Test
	@DisplayName("GET /api/traffic/action returns 403 without authentication")
	void getTrafficAction_unauthorized() throws Exception {
		mockMvc.perform(get("/api/traffic/action"))
				.andExpect(status().isForbidden());
	}

	@Test
	@WithMockUser
	@DisplayName("GET /api/traffic/forecast returns LSTM prediction")
	void getTrafficForecast_success() throws Exception {
		when(lstmPredictorClient.predict(anyList()))
				.thenReturn(List.of(22.45, 11.23, 7.89, 5.34, 4.12));

		mockMvc.perform(get("/api/traffic/forecast"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.predictedDensities").isArray())
				.andExpect(jsonPath("$.status").value("success"));
	}

	@Test
	@WithMockUser
	@DisplayName("GET /api/traffic/forecast returns fallback when LSTM is down")
	void getTrafficForecast_fallback() throws Exception {
		when(lstmPredictorClient.predict(anyList()))
				.thenThrow(new RlInferenceException("Connection refused"));

		mockMvc.perform(get("/api/traffic/forecast"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.status").value(org.hamcrest.Matchers.containsString("fallback")));
	}

	@Test
	@WithMockUser
	@DisplayName("GET /api/traffic/action-enhanced chains LSTM and RL services")
	void getEnhancedTrafficAction_success() throws Exception {
		when(lstmPredictorClient.predict(anyList()))
				.thenReturn(List.of(22.45, 11.23, 7.89, 5.34, 4.12));
		when(rlInferenceClient.predictAction(anyString(), anyList())).thenReturn(2);

		mockMvc.perform(get("/api/traffic/action-enhanced"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.forecastAugmented").value(true))
				.andExpect(jsonPath("$.forecastedDensities").isArray())
				.andExpect(jsonPath("$.signalState").value("GREEN"))
				.andExpect(jsonPath("$.status").value("success"));
	}

	@Test
	@WithMockUser
	@DisplayName("GET /api/traffic/action-enhanced degrades gracefully when LSTM is down")
	void getEnhancedTrafficAction_lstmDown() throws Exception {
		when(lstmPredictorClient.predict(anyList()))
				.thenThrow(new RlInferenceException("LSTM down"));
		when(rlInferenceClient.predictAction(anyString(), anyList())).thenReturn(1);

		mockMvc.perform(get("/api/traffic/action-enhanced"))
				.andExpect(status().isOk())
				.andExpect(jsonPath("$.forecastAugmented").value(false))
				.andExpect(jsonPath("$.signalState").value("YELLOW"))
				.andExpect(jsonPath("$.status").value("success"));
	}
}
