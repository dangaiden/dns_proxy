# Getting Started

I have created 2 alternatives for the same program which are divided in the 2 folders within this zip file.

Basically, the "main_root" **runs the Python program as root on port 53** then, it works out of the box by only changing the name server of the client.

In the other hand, the "main_rootless", is the best approach as it **runs as a non-root user** in a higher port than 1024 which won't run into permissions issues. Only bear in mind that, the port that **this project container uses is 5300** so it won't work out of the box in your PC when you deploy the container (as it doesn't use the default DNS port 53).