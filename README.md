# apsystems_power_local
Home Assistant custom component used to scrape the value of Solar Generated Today: from an APSystems ECU's local web interface (http://{local_ip}/index.php/realtimedata/power_graph).

ECU-R (SunSpec logo/ECU-ID starting with 2162xxxxxxxx)

Make sure that your APSystems ECU-R has this web page visible on your network.

![Screenshot from 2024-01-04 11-04-55](https://github.com/imonlinux/apsystems_power_local/assets/39863321/af5f3887-0866-43d2-bc7f-36e5c2a71810)

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
1. Navigate the the Add Integration page in Settings/Devices & Services.
2. Click Add Integration button at the bottom of the page.
3. Search for APSystems Power Local.
4. Select APSystems Power Local from the list.

![Screenshot from 2024-02-24 18-58-09](https://github.com/imonlinux/apsystems_power_local/assets/39863321/ecf2a5c1-8e3d-47cb-9809-8d08123bfcd2)

5. In the entry form enter the local IP address of your APSystems ECU and click Submit.

![Screenshot from 2024-02-24 18-30-58](https://github.com/imonlinux/apsystems_power_local/assets/39863321/63347cb7-e7b4-40ae-aa29-5d715768cf35)

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

## Your Energy Dashboard should look like this:
![Screenshot from 2024-01-04 11-09-40](https://github.com/imonlinux/apsystems_power_local/assets/39863321/7aea674e-38a4-457d-928c-886fe305040c)


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


## ToDo:

~~Change the sensor state class to total_increasing.~~

~~Implement requirements for installation via HACS~~

--Implement the custom component to allow configuration of the sensor from the UI.--
