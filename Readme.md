# Challenge

## Notes

I have created 2 alternatives for the same program which are divided in the 2 folders within this zip file.

Basically, the "main_root" **runs the Python program as root on port 53** then, it works out of the box by only changing the name server of the client.

In the other hand, the "rootless_alternative", is the best approach as it runs as a **non-root** user in a higher port than 1024 which won't run into permissions issues. Only bear in mind that, the port that **this project container uses is 5300** so it won't work out of the box when you deploy the container.

---

## Asked question

We are also asking you to describe how you will deploy the proxy in a cloud-based infrastructure with various client applications already deployed in it. (Just a text description. You can also attach a scheme/diagram if it makes sense, no strong requirements here).

## Answer


### Location / Security concerns

Regarding the proxy, the best scenario will be within the same network (LAN) where different applications are located:

![Cloud Architecture](/Cloud_architecture_overview.png "Architecture Overview")

This means that if we have different environments (or namespaces in a Kubernetes environment), as they will be in different networks, a proxy for each enviroment will be the best fit to process all the requests from the different applications and to provide security.

The packets between the proxy and the upstream DNS server are sent over an encrypted connection so there is no expected security risks.

In the other hand, in my case where the proxy doesn't support TCP from the client side (LAN), it would be mandatory to do it within the internal network.

As the connection won't be encrypted **between the proxy and the clients (applications)**, it will be vulnerable to a Man-in-the-middle (MITM) attacks as the DNS queries are sent over the plain text connection.

### Deployment

It will be recommeended to deploy it as a micro-service becuase it can escalate quickly and without issues and it doesn't have any more dependencies either as it can run independently.

I would suggest to deploy it as a service in Kubernetes and exposing the port the container is using because in this way, as Kubernetes provides DNS by default on each service, the applications can configure their name servers to that service (Proxy's service name) and as a result, the DNS proxy will handle the traffic between the applications' containers and the upstream DNS server securely.

