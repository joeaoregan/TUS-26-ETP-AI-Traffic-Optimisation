package com.example.gateway.controller;

import com.example.gateway.dto.ErrorResponse;
import com.example.gateway.dto.LoginRequest;
import com.example.gateway.dto.LoginResponse;
import com.example.gateway.security.JwtService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.ExampleObject;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import io.swagger.v3.oas.annotations.media.Schema;

@RestController
@RequestMapping("/api/auth")
@Tag(name = "Authentication")
public class AuthController {

	private final JwtService jwtService;

	@Value("${security.auth.username:admin}")
	private String configuredUsername;

	@Value("${security.auth.password:admin123}")
	private String configuredPassword;

	public AuthController(JwtService jwtService) {
		this.jwtService = jwtService;
	}

	@Operation(summary = "Authenticate user and issue JWT")
	@ApiResponse(responseCode = "200", description = "Authentication successful", content = @Content(mediaType = "application/json", schema = @Schema(implementation = LoginResponse.class), examples = @ExampleObject(value = """
			{
			  \"tokenType\": \"Bearer\",
			  \"accessToken\": \"eyJhbGciOiJIUzI1NiJ9...\",
			  \"expiresIn\": 3600,
			  \"timestamp\": 1710000000000
			}
			""")))
	@ApiResponse(responseCode = "401", description = "Invalid credentials", content = @Content(mediaType = "application/json", schema = @Schema(implementation = ErrorResponse.class), examples = @ExampleObject(value = """
			{
			  \"status\": \"error\",
			  \"message\": \"Invalid username or password\",
			  \"timestamp\": 1710000000000
			}
			""")))
	@PostMapping("/login")
	public ResponseEntity<?> login(@RequestBody LoginRequest request) {
		if (request == null || !StringUtils.hasText(request.getUsername())
				|| !StringUtils.hasText(request.getPassword())) {
			return new ResponseEntity<>(
					new ErrorResponse("error", "Username and password are required", System.currentTimeMillis()),
					HttpStatus.BAD_REQUEST);
		}

		if (!configuredUsername.equals(request.getUsername()) || !configuredPassword.equals(request.getPassword())) {
			return new ResponseEntity<>(
					new ErrorResponse("error", "Invalid username or password", System.currentTimeMillis()),
					HttpStatus.UNAUTHORIZED);
		}

		String token = jwtService.generateToken(request.getUsername());
		LoginResponse response = new LoginResponse("Bearer", token, jwtService.getExpirationSeconds(),
				System.currentTimeMillis());
		return ResponseEntity.ok(response);
	}
}
