FROM python:3.5.1-alpine

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip \
  && pip install --no-cache -r requirements.txt \
  && pip install --no-cache mock nose \
  && nosetests \
  && rm -rf /app/tests \
  && pip uninstall -y mock nose

CMD ["python", "-m", "makobot"]