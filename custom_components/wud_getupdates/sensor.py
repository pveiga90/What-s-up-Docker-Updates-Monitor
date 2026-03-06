import logging
import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "wud_getupdates"

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities):
    """Set up the WUD sensor platform."""
    wud_host = config_entry.data["host"]
    wud_port = config_entry.data["port"]
    instance_name = config_entry.data["instance_name"]  # Get instance name

    # Fetch container information from WUD API
    containers = await get_containers(wud_host, wud_port)

    # Create a sensor for each container and assign it to the instance name device
    sensors = []
    for container in containers:
        sensors.append(WUDContainerSensor(container, config_entry, instance_name))
    
    async_add_entities(sensors, True)

async def get_containers(host, port):
    """Fetch containers from the WUD API.

    The host argument may include a scheme (http:// or https://). If no scheme
    is provided we default to http. The port value is optional; if it's empty or
    evaluates to False we omit the ":port" portion of the URL entirely.
    """
    # remove any trailing slashes so concatenation below is clean
    host = host.rstrip("/")

    # ensure we have a scheme
    if not host.lower().startswith(("http://", "https://")):
        host = "http://" + host

    # construct base URL and append port only when it's set
    if port:
        url = f"{host}:{port}/api/containers"
    else:
        url = f"{host}/api/containers"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    _LOGGER.error(
                        "Failed to fetch containers from WUD at %s - HTTP %s: %s",
                        url,
                        response.status,
                        await response.text(),
                    )
                    return []
    except Exception as err:
        _LOGGER.error(
            "Unexpected error when fetching containers from WUD at %s: %s",
            url,
            err,
        )
        return []

class WUDContainerSensor(SensorEntity):
    """Representation of a What's Up Docker container sensor."""

    def __init__(self, container, config_entry: ConfigEntry, instance_name: str):
        """Initialize the sensor."""
        self._container = container
        self._config_entry = config_entry
        self._name = f"{container['name']} Update Available"
        self._state = container.get("updateAvailable", False)
        self._unique_id = f"wud_{container['id']}_update_available"
        self._instance_name = instance_name

        # Device info for Home Assistant, now using the instance name
        self._device_info = {
            "identifiers": {(DOMAIN, config_entry.entry_id)},
            "name": instance_name,  # Use the instance name as the device name
            "manufacturer": "What's Up Docker",
            "model": "Docker Instance",
        }

    @property
    def unique_id(self):
        """Return a unique ID for this sensor."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return "Yes" if self._state else "No"

    @property
    def device_info(self):
        """Return the device info to which this entity belongs."""
        return self._device_info

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        return {
            "container_id": self._container["id"],
            "version": self._container.get("version", "unknown"),
            "update_available": self._state,
        }
