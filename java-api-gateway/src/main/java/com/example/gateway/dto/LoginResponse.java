package com.example.gateway.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Schema(description = "Authentication response payload")
public class LoginResponse {

    @Schema(description = "JWT token type", example = "Bearer")
    private String tokenType;

    @Schema(description = "Signed JWT access token")
    private String accessToken;

    @Schema(description = "Token validity in seconds", example = "3600")
    private long expiresIn;

    @Schema(description = "Unix timestamp", example = "1710000000000")
    private long timestamp;
}
