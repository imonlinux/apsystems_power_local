# apsystems_power_local
Home Assistant custom component used to scrape the value of Solar Generated Today: from an APSystems EMU's local web interface (http://{local_ip}/index.php/realtimedata/power_graph

This custom component is currently working on my HA system:
Core 2023.12.4
Supervisor 2023.12.0
Operating System 11.2
Frontend 20231208.2

Component requires you to put the following sensor in your configuration.yaml file:

sensor:
  - platform: apsystems_power_local
    ip_address: "192.168.1.234"  # Replace with your device's IP address


I am working to implement the custom component to allow configuration of the sensor from the UI.
