# apsystems_power_local
Home Assistant custom component used to scrape the value of Solar Generated Today: from an APSystems ECU's local web interface (http://{local_ip}/index.php/realtimedata/power_graph).

ECU-R (SunSpec logo/ECU-ID starting with 2162xxxxxxxx)

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


## HACS Installation Instructions
To install this component via HACS:
1. Open HACS in Home Assistant.
2. Go to "Integrations" and click on the "+ ADD" button at the bottom right corner.
3. Search for "APSystems Power Local" and select it.
4. Click on "Install".

## Configuration
After installation, you need to configure the component:
- If your component requires configuration in `configuration.yaml`, add the necessary lines.
- For UI configuration, go to 'Configuration' -> 'Integrations' -> 'Add Integration', and then select "APSystems Power Local".

## Usage
Provide examples of how to use your component, such as Lovelace UI configurations or automations.

## Troubleshooting and Support
For common issues and their resolutions, [visit this link](https://github.com/imonlinux/apsystems_power_local).
To report issues or seek support, please use the [issue tracker](https://github.com/imonlinux/apsystems_power_local/issues).

## Contributing
Contributions to this project are welcome! To contribute, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request.

## Changelog
For information about the latest changes and updates, refer to the [changelog](https://github.com/imonlinux/apsystems_power_local/releases).
