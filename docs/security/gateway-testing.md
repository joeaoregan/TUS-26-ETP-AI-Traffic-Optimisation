# Testing

The root-level `test_api.py` script has been updated to:

- Authenticate first using JWT credentials
- Cache the returned access token
- Send the token on protected requests
- **Display color-coded output for better readability**
- **Track test results (e.g., "All tests passed! 4/4")**
- **Return boolean status for each test function**

Run it from the repository root:

```bash
python test_api.py
```
Test output includes:

✅ Green checkmarks for successful operations  
❌ Red X marks for failures  
🔵 Blue headers for test sections  
🔄 Test counter showing passed/total tests  

## Requirements

To use the enhanced test script with color output, install colorama:

## Relevant Files

- `src/main/java/com/example/gateway/controller/AuthController.java`
- `src/main/java/com/example/gateway/config/SecurityConfig.java`
- `src/main/java/com/example/gateway/security/JwtService.java`
- `src/main/java/com/example/gateway/security/JwtAuthenticationFilter.java`
- `src/main/resources/application.yml`
- `src/main/resources/application-prod.yml`
- `src/main/java/com/example/gateway/dto/LoginRequest.java`
- `src/main/java/com/example/gateway/dto/LoginResponse.java`
- `src/main/java/com/example/gateway/dto/ErrorResponse.java`
- `test_api.py`

## Current Limitations

- Single configured user only
- No user database integration
- No role-based authorization
- No refresh tokens
- No logout endpoint because the system is stateless

If the project needs stronger access control later, the next logical step is to replace configured credentials with a persistent user store and add roles.
