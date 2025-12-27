FROM public.ecr.aws/lambda/python:3.12

COPY validation/requirements.txt ${LAMBDA_TASK_ROOT}/requirements_common.txt

RUN pip install -r requirements_common.txt

COPY validation ${LAMBDA_TASK_ROOT}/validation
COPY login_lambda/src ${LAMBDA_TASK_ROOT}

CMD ["login_lambda.lambda_handler"]
