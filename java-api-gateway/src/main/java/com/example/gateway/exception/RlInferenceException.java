package com.example.gateway.exception;

/**
 * Custom exception for RL Inference errors.
 */
public class RlInferenceException extends RuntimeException {
    private static final long serialVersionUID = 1L;

    public RlInferenceException(String message) {
        super(message);
    }

    public RlInferenceException(String message, Throwable cause) {
        super(message, cause);
    }
}