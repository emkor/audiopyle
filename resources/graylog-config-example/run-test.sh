sudo docker build -t test .
sudo docker create -it --name testcontainer test
sudo docker start testcontainer

sudo docker run -it --log-driver=gelf --log-opt gelf-address=udp://0.0.0.0:12201 test python print.py 
