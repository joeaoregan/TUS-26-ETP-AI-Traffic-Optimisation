package com.example.gateway.config;

import java.util.List;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import io.swagger.v3.oas.models.servers.Server;

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
		Server localServer = new Server().url("http://localhost:8080").description("Local development server");
		Server productionServer = new Server().url("https://ai-traffic-control-api.onrender.com")
				.description("Production Cloud server (Render)");

		return new OpenAPI()
				.components(new Components().addSecuritySchemes("bearerAuth",
						new SecurityScheme().type(SecurityScheme.Type.HTTP).scheme("bearer").bearerFormat("JWT")
								.description("JWT Bearer token authentication")))
				.addSecurityItem(new SecurityRequirement().addList("bearerAuth"))
				.info(new Info().title(apiTitle).description(apiDescription).version(apiVersion)
						.contact(new Contact().name(appAuthors).email(appEmail)))
				.servers(List.of(productionServer, localServer));
	}
}
