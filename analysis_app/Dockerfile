FROM python:3.10.4-slim-bullseye

WORKDIR /usr/src/phenodb_analysis

COPY analysis_utils.py .
COPY analyzer.py .
COPY compound_analysis_utils.py .
COPY log.py .
COPY main.py .
COPY sample_maker.py .
COPY utils.py .
COPY variant_excluder.py .
COPY variant_fields.py .

RUN apt update && \
	DEBIAN_FRONTEND="noninteractive" TZ="America/New_York"

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pytz