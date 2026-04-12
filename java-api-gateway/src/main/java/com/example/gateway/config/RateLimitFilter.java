package com.example.gateway.config;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Simple in-memory rate limiter using a sliding window.
 * Limits each IP to a configurable number of requests per minute.
 * Protects the inference pipeline from abuse as discussed in Section VI.
 */
@Component
public class RateLimitFilter implements Filter {

	private static final int MAX_REQUESTS_PER_MINUTE = 60;
	private static final long WINDOW_MS = 60_000;

	private final Map<String, WindowCounter> counters = new ConcurrentHashMap<>();

	@Override
	public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
			throws IOException, ServletException {

		String clientIp = request.getRemoteAddr();
		WindowCounter counter = counters.computeIfAbsent(clientIp, k -> new WindowCounter());

		if (counter.tryAcquire()) {
			chain.doFilter(request, response);
		} else {
			HttpServletResponse httpResponse = (HttpServletResponse) response;
			httpResponse.setStatus(429);
			httpResponse.setContentType("application/json");
			httpResponse.getWriter().write(
					"{\"status\":\"error\",\"message\":\"Rate limit exceeded. Max "
							+ MAX_REQUESTS_PER_MINUTE + " requests per minute.\"}");
		}
	}

	private static class WindowCounter {
		private final AtomicInteger count = new AtomicInteger(0);
		private volatile long windowStart = System.currentTimeMillis();

		boolean tryAcquire() {
			long now = System.currentTimeMillis();
			if (now - windowStart > WINDOW_MS) {
				synchronized (this) {
					if (now - windowStart > WINDOW_MS) {
						count.set(0);
						windowStart = now;
					}
				}
			}
			return count.incrementAndGet() <= MAX_REQUESTS_PER_MINUTE;
		}
	}
}
