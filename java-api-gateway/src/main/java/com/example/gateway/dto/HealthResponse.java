package com.example.gateway.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Schema(description = "Health check response")
public class HealthResponse {

    @Schema(description = "Overall system status — healthy only if all services are up", example = "healthy")
    private String status;

    @Schema(description = "RL inference service status", example = "up")
    private String inferenceService;

    @Schema(description = "LSTM predictor service status", example = "up")
    private String lstmPredictorService;

    @Schema(description = "Unix timestamp", example = "1710000000000")
    private long timestamp;
}
