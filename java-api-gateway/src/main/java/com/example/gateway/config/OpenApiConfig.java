package com.example.gateway.config;

import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.servers.Server;
import io.swagger.v3.oas.models.OpenAPI;

import java.util.List;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class OpenApiConfig {

	@Value("${api.title}")
	private String apiTitle;

	@Value("${api.description}")
	private String apiDescription;

	@Value("${api.version}")
	private String apiVersion;

	@Value("${api.authors}")
	private String appAuthors;

	@Value("${api.email}")
	private String appEmail;

	@Bean
	OpenAPI trafficControlApi() {
		return new OpenAPI()
				.info(new Info().title(apiTitle)
						.description(
								"""
										This API provides traffic signal control capabilities powered by a Reinforcement Learning (RL) inference service.

										## Overview
										The system simulates or accepts real-time traffic observations and uses an RL model to predict the optimal traffic signal action.
										These predictions help manage congestion, improve flow efficiency, and support adaptive traffic control strategies.

										## Key Features
										- **Automatic traffic signal prediction** using RL inference.
										- **Support for custom observation inputs** for testing and experimentation.
										- **Health monitoring** to verify the availability of the inference service.
										- **Structured success and error responses** for consistent API behavior.

										## Endpoints
										- **GET /api/traffic/action** — Generates dummy observations and returns a predicted traffic signal state.
										- **POST /api/traffic/action** — Accepts custom observations and returns a model prediction.
										- **GET /api/traffic/health** — Reports the health status of the RL inference service.

										This API is designed for academic, experimental, and demonstration purposes within a cloud‑native microservices architecture.
										""")
						.version(apiVersion).contact(new Contact().name(appAuthors).email(appEmail)))
				.servers(List.of(new Server().url("http://localhost:8080").description("Local development server")));
	}
}
