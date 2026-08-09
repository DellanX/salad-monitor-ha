# Salad GPU Monitor - Home Assistant Integration

[![Add to HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=dellanx&repository=salad-monitor-ha&category=integration)

This custom integration connects Home Assistant to the Salad GPU Monitor service.

The integration supports both the legacy `/health` endpoint and the new `/api/v1/health` endpoint, and exposes the expanded v1 monitoring state (wallet, job, download, hardware, network, GPU demand, process, and warning metrics) as Home Assistant entities.

## Installation (HACS)

1. Open HACS → Integrations
2. Go to **Custom Repositories**
3. Add: https://github.com/dellanx/salad-monitor-ha
4. Category: **Integration**
5. Install “Salad GPU Monitor”
6. Restart Home Assistant

## Configuration

1. Go to **Settings → Devices & Services**
2. Click **Add Integration**
3. Search for **Salad GPU Monitor**
4. Enter:

- Host (IP of the machine running salad-monitor)
- Port (default: 8000)

## Requirements

You must be running the Salad Monitor service: ghcr.io/dellanx/salad-monitor:latest
