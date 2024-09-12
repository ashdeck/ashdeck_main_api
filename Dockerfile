FROM public.ecr.aws/lambda/python:3.10
COPY ./ ./
COPY requirements.txt requirements.txt
RUN pip install -r ./requirements.txt
CMD ["main.handler"]
