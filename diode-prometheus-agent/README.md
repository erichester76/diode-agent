# Diode Prometheus  Agent

The Diode prometheus Agent is a lightweight network device discovery tool that uses [prometheus](https://github.com/prometheus/prometheus) to streamline data entry into NetBox through the [Diode](https://github.com/netboxlabs/diode) ingestion service.

# Get started

This is a basic set of instructions to get started using Diode prometheus agent on a local machine.

## Requirements

The Diode prometheus Agent requires a Python runtime environment and has the following requirements:
- netboxlabs-diode-sdk==0.1.0
- pydantic==2.7.1
- python-dotenv==1.0.1

Instructions on installing the Diode SDK Python can be found [here](https://github.com/netboxlabs/diode-sdk-python).

## Installation

Clone the agent repository:

```bash
git clone https://github.com/netboxlabs/diode-agent.git
cd diode-agent/
```

Create a Python virtual environment and install the agent:

```bash
python3 -m venv venv
source venv/bin/activate
pip install ./diode-prometheus-agent --no-cache-dir
```

### Create a discovery configuration file

A configuration file needs to be created with an inventory of devices to be discovered. An example (`config.sample.yaml`) is provided in the agent repository. The `config` section needs to be updated to reflect your Diode server environment and the `data` section should include a list of all devices (and their credentials) to be discovered.

```yaml
diode:
  config:
    target: ${DIODE_URL}
    api_key: ${DIODE_API_KEY}
  policies:
    discovery_1:
      config:
        netbox:
          site: New York NY
      data:
          optional_args:
            enable_password: ${ARISTA_PASSWORD}
```

Variables (using `${ENV}` syntax) can be referenced in the configuration file from environmental variables or from a provided `.env` file.


## Running the agent

Usage:

```
usage: diode-prometheus-agent [-h] [-V] -c config.yaml [-e .env] [-w N]

Diode Agent for prometheus

options:
  -h, --help            show this help message and exit
  -V, --version         Display Diode Agent, prometheus and Diode SDK versions
  -c config.yaml, --config config.yaml
                        Agent yaml configuration file
  -e .env, --env .env   File containing environment variables
  -w N, --workers N     Number of workers to be used
```

Run `diode-prometheus-agent` with a discovery configuration file named `config.yaml`:

```bash
diode-prometheus-agent -c config.yaml
```

The Diode prometheus agent tries to fetch information from network devices about the following NetBox object types:

- [Virtualization.Cluster](https://netboxlabs.com/docs/netbox/en/stable/models/virtualization/cluster/)
- [Virtualization.ClusterGroup](https://netboxlabs.com/docs/netbox/en/stable/models/virtualization/clustergroup/)
- [Virtualization.ClusterType](https://netboxlabs.com/docs/netbox/en/stable/models/virtualization/clustertype/)
- [Virtualization.VirtualMachine](https://netboxlabs.com/docs/netbox/en/stable/models/virtualization/virtualmachine/)
- [Virtualization.VirtualDisk](https://netboxlabs.com/docs/netbox/en/stable/models/virtualization/virtualmachine/)
- [Virtualization.VMInterface](https://netboxlabs.com/docs/netbox/en/stable/models/virtualization/vminterface/)
- [Virtualization.Datastore]*if netbox-storage-plugin is installed 

- [DCIM.Device](https://netboxlabs.com/docs/netbox/en/stable/models/dcim/device/)
- [DCIM.DeviceType](https://netboxlabs.com/docs/netbox/en/stable/models/dcim/devicetype/)
- [DCIM.Interface](https://netboxlabs.com/docs/netbox/en/stable/models/dcim/interface/)
- [DCIM.Cable](https://netboxlabs.com/docs/netbox/en/stable/models/dcim/cable/)
- [DCIM.Platform](https://netboxlabs.com/docs/netbox/en/stable/models/dcim/platform/)

- [Storage.Disk]*if netbox-storage-plugin is installed 
- [Storage.Controller]*if netbox-storage-plugin is installed 
- [Storage.DiskGroup]*if netbox-storage-plugin is installed 
- [Storage.LogicalDisk]*if netbox-storage-plugin is installed 
- [Storage.Partition]*if netbox-storage-plugin is installed 
- [Storage.Share]*if netbox-storage-plugin is installed 

- [IPAM.IPAddress](https://netboxlabs.com/docs/netbox/en/stable/models/ipam/ipaddress/)
- [IPAM.Prefix](https://netboxlabs.com/docs/netbox/en/stable/models/ipam/prefix/)
- [IPAM.Vlan](https://netboxlabs.com/docs/netbox/en/stable/models/ipam/vlan/)

## License

Distributed under the Apache 2.0 License. See [LICENSE.txt](./diode-proto/LICENSE.txt) for more information.
