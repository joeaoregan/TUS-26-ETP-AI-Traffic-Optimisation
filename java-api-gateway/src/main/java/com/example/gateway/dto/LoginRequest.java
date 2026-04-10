package com.example.gateway.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Schema(description = "Authentication request payload")
public class LoginRequest {

    @Schema(description = "API username", example = "admin")
    private String username;

    @Schema(description = "API password", example = "admin123")
    private String password;
}
