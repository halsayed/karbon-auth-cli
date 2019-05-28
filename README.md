# karbon-auth-cli
Python script to generate Nutanix Karbon kubeconfig

## Installation

Python3 and pip are required to run this script. To run locally:
```
git clone https://github.com/halsayed/karbon-auth-cli.git
cd karbon-auth-cli
pip3 install -r requirements.txt
```

## Usage
You can execute the script as follows:
```
python3 karbon-auth.py PC_HOST KARBON_CLUSTER_NAME -u USERNAME -p PASSWORD

```

An alternative method is available to run the script inside a docker container
```
docker run --rm hexadtech/karbon-auth PC_HOST KARBON_CLUSTER_NAME -u USERNAME -p PASSWORD
```

Kubeconfig yaml file is output to the stdout, you can save to a file and export KUBECONFIG or move it to $HOME/.kube

## License
[MIT](https://choosealicense.com/licenses/mit/)