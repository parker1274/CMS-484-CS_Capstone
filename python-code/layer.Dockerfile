FROM public.ecr.aws/lambda/python:3.9

RUN yum update -y
RUN yum install -y \
    python3 \
    python3-pip \
    gcc \
    python3-dev \
    musl-dev

COPY requirements.txt ${LAMBDA_TASK_ROOT}/

RUN python3 -m pip install --upgrade pip && \
    pip install awslambdaric boto3 && \
    pip install -r requirements.txt
