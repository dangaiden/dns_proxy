#  Pull lightweight image
FROM python:3.7-alpine

#  Update and install openssl package
RUN apk update && apk add openssl

# Work directory for our application
RUN adduser -D pyuser
USER pyuser
WORKDIR /home/pyuser/
ENV PATH="/home/pyuser/.local/bin:${PATH}"

# Install dependency
RUN pip3 install --user dnspython

COPY --chown=pyuser:pyuser dns_stub_rootless.py .

EXPOSE 5300

CMD ["python3","dns_stub_rootless.py"]