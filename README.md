# apsystems_power_local
Home Assistant custom component used to scrape the value of Solar Generated Today: from an APSystems ECU's local web interface (http://{local_ip}/index.php/realtimedata/power_graph).

ECU-R (SunSpec logo/ECU-ID starting with 2162xxxxxxxx)

This custom component is currently working on my HA system:
```
Core 2024.1.0
Supervisor 2023.12.0
Operating System 11.2
Frontend 20240103.3
```

## Manual Installation:

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
## HACS Installation Instructions
To manually add this repository to HACS and install the component:

1. Open HACS in Home Assistant.
2. Navigate to "Integrations" section.
3. In the top right corner, click on the three dots and select "Custom repositories".
4. In the dialog that appears, paste the URL of this repository (`https://github.com/imonlinux/apsystems_power_local`) into the 'Repository' field.
5. Select 'Integration' as the category.
6. Click 'Add'.
7. The component should now appear in the HACS integrations list. Search for "APSystems Power Local" and select it.
8. Click on "Install" to install the component.

Once installed, you can proceed with the configuration steps as outlined in this README.

## Configuration
After installation, you need to configure the component:
- This component requires configuration in `configuration.yaml`, add the necessary lines.
```yaml
sensor:
  - platform: apsystems_power_local
    ip_address: "192.168.1.234"  # Replace with your device's IP address
```

### Restart Home Assistant.

## Usage
To add the APSystems Power entity to the Energy Dashboard for solar energy monitoring, follow these steps:
1. Ensure that the `apsystems_power_local` component is correctly installed and configured.
2. Navigate to the Energy Dashboard in your Home Assistant interface.
3. Click on 'Settings' in the top right corner of the Energy Dashboard.
4. Under 'Solar Panels', select 'Add Solar Production'.
5. From the list of available entities, choose the `APSystems Power` entity.
6. Follow the prompts to configure and add the entity to your Energy Dashboard.
7. Once added, your Energy Dashboard will display solar energy production data from your APSystems device.

## Configuration
After installation, you need to configure the component:
- This component requires configuration in `configuration.yaml`, add the necessary lines.
```yaml
sensor:
  - platform: apsystems_power_local
    ip_address: "192.168.1.234"  # Replace with your device's IP address
```
## Usage
To add the APSystems Power entity to the Energy Dashboard for solar energy monitoring, follow these steps:
1. Ensure that the `apsystems_power_local` component is correctly installed and configured.
2. Navigate to the Energy Dashboard in your Home Assistant interface.
3. Click on 'Settings' in the top right corner of the Energy Dashboard.
4. Under 'Solar Panels', select 'Add Solar Production'.
5. From the list of available entities, choose the `APSystems Power` entity.
6. Follow the prompts to configure and add the entity to your Energy Dashboard.
7. Once added, your Energy Dashboard will display solar energy production data from your APSystems device.


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


ToDo:

~~Change the sensor state class to total_increasing.~~

Implement the custom component to allow configuration of the sensor from the UI.

Implement requirements for installation via HACS
