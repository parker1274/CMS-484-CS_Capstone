FROM 471112589532.dkr.ecr.us-east-1.amazonaws.com/nba_layer:latest

WORKDIR ${LAMBDA_TASK_ROOT}

RUN echo $(pwd)

COPY . ${LAMBDA_TASK_ROOT}/

ENV MPLCONFIGDIR="/tmp/matplotlib"

# # TO ACCESS THE CONTAINER LOCALLY REMOVE THIS LINE AND UNCOMMENT THE NEXT TWO
CMD [ "main.lambda_handler" ]
# ENTRYPOINT []
# CMD ["tail", "-f", "/dev/null"]