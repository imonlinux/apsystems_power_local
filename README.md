# apsystems_power_local
Home Assistant custom component used to scrape the value of Solar Generated Today: from an APSystems ECU's local web interface (http://{local_ip}/index.php/realtimedata/power_graph).

This custom component is currently working on my HA system:
```
Core 2023.12.4
Supervisor 2023.12.0
Operating System 11.2
Frontend 20231208.2
```

Installation:

Copy the apsystems_power_local folder into the Custom Compenents folder of you HA instance.

```
/homeassistant/custom_components/apsystems_power_local
```
 The foler apsystems_power_local should contain the files:
 ```markdown
custom_components/
│
└─── apsystems_power_local/
    │   __init__.py
    │   manifest.json
    │   sensor.py
    │   const.py
```

Component requires you to put the following sensor in your configuration.yaml file:

```yaml
sensor:
  - platform: apsystems_power_local
    ip_address: "192.168.1.234"  # Replace with your device's IP address
```

ToDo:

~~Change the sensor state class to total_increasing.~~

Implement the custom component to allow configuration of the sensor from the UI.
