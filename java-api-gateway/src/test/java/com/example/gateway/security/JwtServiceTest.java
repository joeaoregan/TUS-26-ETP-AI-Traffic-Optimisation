package com.example.gateway.security;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class JwtServiceTest {

	private JwtService jwtService;

	@BeforeEach
	void setUp() {
		jwtService = new JwtService();
		try {
			var secretField = JwtService.class.getDeclaredField("jwtSecret");
			secretField.setAccessible(true);
			secretField.set(jwtService, "test-secret-key-that-is-long-enough-for-hs256-signing");

			var expirationField = JwtService.class.getDeclaredField("expirationMinutes");
			expirationField.setAccessible(true);
			expirationField.set(jwtService, 60L);

			var issuerField = JwtService.class.getDeclaredField("issuer");
			issuerField.setAccessible(true);
			issuerField.set(jwtService, "test-issuer");

			jwtService.initialize();
		} catch (Exception e) {
			fail("Failed to set up JwtService: " + e.getMessage());
		}
	}

	@Test
	@DisplayName("Generated token is valid")
	void generateAndValidateToken() {
		String token = jwtService.generateToken("admin");
		assertTrue(jwtService.isTokenValid(token));
	}

	@Test
	@DisplayName("Username can be extracted from token")
	void extractUsername() {
		String token = jwtService.generateToken("testuser");
		assertEquals("testuser", jwtService.extractUsername(token));
	}

	@Test
	@DisplayName("Malformed token returns invalid")
	void malformedToken() {
		assertFalse(jwtService.isTokenValid("not.a.valid.token"));
	}

	@Test
	@DisplayName("Expiration seconds are correctly calculated")
	void expirationSeconds() {
		assertEquals(3600, jwtService.getExpirationSeconds());
	}

	@Test
	@DisplayName("Different users get different tokens")
	void differentUsersGetDifferentTokens() {
		String token1 = jwtService.generateToken("user1");
		String token2 = jwtService.generateToken("user2");
		assertNotEquals(token1, token2);
		assertEquals("user1", jwtService.extractUsername(token1));
		assertEquals("user2", jwtService.extractUsername(token2));
	}
}
