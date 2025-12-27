# Project Structure and Build Instructions

The project has been restructured to support multiple Lambda functions with shared validation logic, using a layout suitable for Docker build contexts.

## Directory Structure

```text
lambda_functions/
├── validation/
│   ├── src/
│   │   ├── pydantic_validation.py  # Common validation logic
│   │   └── calculator_data.py      # Shared data models
│   └── requirements.txt            # Common dependencies (pydantic)
├── calculator_sns/
│   ├── src/
│   │   └── calculator_sns.py
│   └── Dockerfile
├── refresh_lambda/
│   ├── src/
│   │   ├── refresh_lambda.py
│   │   └── refresh_data.py         # Specific data model
│   └── Dockerfile
├── login_lambda/
│   ├── src/
│   │   ├── login_lambda.py
│   │   └── login_data.py           # Specific data model
│   └── Dockerfile
└── lambda_test_http/
    ├── src/
    │   └── lambda_test_http.py
    └── Dockerfile
```

## Building Docker Images

**Important:** You must be in the `lambda_functions` directory (root of the structure) to build the images. The build context must be the `lambda_functions` directory so that the Dockerfiles can access the common `validation` directory.

### Build Commands

Run the following commands from the `lambda_functions` directory:

**Calculator SNS:**
```bash
docker build -t calculator_sns -f calculator_sns/Dockerfile .
```

**Refresh Lambda:**
```bash
docker build -t refresh_lambda -f refresh_lambda/Dockerfile .
```

**Login Lambda:**
```bash
docker build -t login_lambda -f login_lambda/Dockerfile .
```

**Lambda Test HTTP:**
```bash
docker build -t lambda_test_http -f lambda_test_http/Dockerfile .
```

## Notes
- The `Dockerfile` for each lambda copies the common `validation` directory and requirements into the image.
- Specific source code is copied to the root of the Lambda task (`${LAMBDA_TASK_ROOT}`).
- This setup ensures `from validation.src...` imports work correctly alongside local relative imports like `from refresh_data...`.
