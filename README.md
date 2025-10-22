# Time Machine G2 Raceclock Controller

A cross-platform desktop app for fully controlling the Electro-Numerics Raceclock Time Machine G2.  
Features real-time serial comms, CSV import, PDF/.hy3 export, event seeding, DQ management, and direct thermal printing.

## Features

- RS-232/USB serial communication with Raceclock G2
- Live timer display and full control (start, stop, reset, splits)
- Import entries from CSV; seed events and heats
- Export results as PDF, Hy-Tek Meet Manager (.hy3)
- Manage DQs, heats, psych sheets
- Print results to the Time Machine's thermal printer
- Event logging and robust error handling
- Cross-platform: Windows, Linux, macOS

## Developer Setup

```bash
git clone https://github.com/YOUR-USER/raceclock-g2-controller.git
cd raceclock-g2-controller
python -m venv env
source env/bin/activate   # or .\env\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

## File Structure

- `main.py` – App entry point
- `gui/` – All GUI panels, PyQt5/6 widgets
- `core/` – Serial comms, protocol, hardware integration
- `io/` – File import/export (CSV, PDF, HY3)
- `utils/` – Error handling, installer
- `tests/` – Unit tests
- `resources/` – Icons and static assets

## Contributing

Pull requests welcome!  
Please open issues for bugs and feature requests.

## License

[MIT](LICENSE)
