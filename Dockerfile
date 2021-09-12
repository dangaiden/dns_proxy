### This image is only for development purposes.
### Running as root is not the best solution but it solves the issue
### to deal with lower ports than 1024.

#  Pull lightweight image
FROM python:3.7-alpine

#  Update and install openssl package
RUN apk update && apk add openssl

# Work directory for our application
WORKDIR /usr/local/bin

# We do it as root although a warning will appear as it's not recommended.
RUN pip3 install --user dnspython

COPY dns_stub_resolver.py .

CMD ["python3","dns_stub_resolver.py"]