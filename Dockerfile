FROM python:3.12-slim as base
WORKDIR /app

ARG UID=1001
ARG GID=1001

ENV PORT 8000
ENV PYTHONUNBUFFERED 0
ENV PYTHONDONTWRITEBYTECODE 1
ENV NONROOT_PATH="/home/nonroot"
ENV NONROOT_BIN_PATH="${NONROOT_PATH}/.local/bin"
ENV PATH="${NONROOT_BIN_PATH}:${PATH}"

RUN addgroup --gid $GID nonroot \
    && adduser --uid $UID --gid $GID --disabled-password --gecos "" nonroot \
    && mkdir -p /home/nonroot/.pip $NONROOT_BIN_PATH


FROM base as package-installation

COPY requirements /app/requirements

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && pip install --upgrade pip \
    && pip install -r /app/requirements/production.txt \
    && apt-get remove -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*


FROM base

COPY --from=package-installation /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=package-installation /usr/local/bin/ $NONROOT_BIN_PATH
COPY . .

RUN chown -R $UID:$GID /app

EXPOSE $PORT/tcp
USER nonroot

ENTRYPOINT ["/app/scripts/startup.sh"]
