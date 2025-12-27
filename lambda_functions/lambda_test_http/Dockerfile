FROM public.ecr.aws/lambda/python:3.12

COPY validation/requirements.txt ${LAMBDA_TASK_ROOT}/requirements_common.txt

RUN pip install -r requirements_common.txt

COPY validation ${LAMBDA_TASK_ROOT}/validation
COPY lambda_test_http/src ${LAMBDA_TASK_ROOT}

CMD ["lambda_test_http.lambda_handler"]
