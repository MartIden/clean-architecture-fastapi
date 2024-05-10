################
# STAGE: BUILD #
################

FROM python:3.11 as builder

LABEL org.opencontainers.image.authors="Roman Morozkin <romasa464@gmail.com>"

# INSTAL SYSTEM DEPENDENCIES
RUN apt-get clean -y \
    && apt-get update -y \
    && apt-get install -y --no-install-recommends  \
      apt-transport-https=2.\* \
      build-essential=12.9 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /install
COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r /install/requirements.txt


################
# STAGE: FINAL #
################

FROM python:3.11-slim as final

COPY --from=builder /install /usr/local
COPY .. /app

WORKDIR /app

RUN apt-get clean -y \
  && apt-get update -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && addgroup --gid 1000 editorconfig \
  && adduser \
    --uid 1000 \
    --home /home/editorconfig \
    --shell /bin/sh \
    --ingroup editorconfig \
    --disabled-password \
    romasa464\
  && chown -R 1000:1000 /app

USER romasa464

EXPOSE 5050

ENTRYPOINT ["uvicorn"]
CMD ["src.kernel.fastapi.run:app", "--host", "0.0.0.0", "--port", "5005", "--reload", "--log-level", "error"]
