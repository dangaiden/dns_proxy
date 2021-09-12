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

If we talk in the cloud without a Kubernetes environment, the best scenario will be within the same network (LAN) where different applications are located:

![Cloud Architecture](/Cloud_architecture_overview.png "Architecture Overview")

This means that if we have different environments, as they will be in different networks, a proxy for each enviroment will be the best fit to process all the requests from the different applications and to provide security.

---

About how the DNS proxy works, in summary:

The packets between the proxy and the upstream DNS server are sent over an encrypted connection so there is no expected security risks.

In the other hand, in my case where the proxy doesn't support TCP from the client side (LAN), it would be mandatory to do it within the internal network.

As the connection won't be encrypted **between the proxy and the clients (applications)**, it will be vulnerable to a Man-in-the-middle (MITM) attacks as the DNS queries are sent over the plain text connection.

### Deployment

If we have an environment already deployed with micro-services in Kubernetes, then, the best thing will be to deploy this container within a pod for each node.

Then in Kubernetes terms, it will require to apply a DaemonSet (to ensure all Nodes run a copy of a Pod) and then configure Kubernetes DNS (CoreDNS) to point to our proxy-dns.

There is more information about how it works [here](https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/) but, basically changing the configmap of the CoreDNS service will apply it to all pods within the Kubernetes cluster.
