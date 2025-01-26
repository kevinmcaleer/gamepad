### **Modules and Libraries**

1. **`machine`**  
   Provides access to hardware components like pins and I2C.
   
2. **`aioble`**  
   Simplifies working with BLE (Bluetooth Low Energy) functionality.

3. **`asyncio`**  
   Enables asynchronous programming for tasks like button monitoring and BLE connection.

4. **`micropython.const`**  
   Optimizes constant values for memory efficiency in MicroPython.

5. **`bluetooth`**  
   Handles BLE UUIDs and device interactions.

6. **`time.ticks_ms` and `time.ticks_diff`**  
   Provides millisecond-level timing for precise event handling.

7. **`ssd1306`**  
   A library to interface with SSD1306 OLED displays via I2C.

---

### **Classes**

#### **1. `Button`**

Handles button press detection with debounce.

- **Attributes**:
  - `pin`: The GPIO pin connected to the button.
  - `debounce_ms`: Debounce duration in milliseconds (default: 50 ms).
  - `_last_pressed`: Timestamp of the last valid button press.
  - `_was_pressed`: Tracks the previous button state.

- **Methods**:
  - `is_pressed()`: Checks if the button is currently pressed, considering debounce.
  - `state_changed()`: Returns a tuple indicating button press/release events.

#### **2. `GamePad`**

Represents the hardware interface for a gamepad with buttons, BLE communication, and an OLED display.

- **Attributes**:
  - `buttons`: A dictionary of `Button` objects for each gamepad button.
  - `led`: Onboard LED for status indication.
  - `connected`: Tracks BLE connection status.
  - `connection`: Active BLE connection object.
  - `device_info`: BLE service for the gamepad.
  - `button_characteristic`: BLE characteristic to send button states.
  - `oled`: SSD1306 OLED display instance.

- **Methods**:
  - `monitor_buttons()`: Continuously monitors button states and updates the OLED/BLE.
  - `peripheral_task()`: Advertises the BLE service and handles incoming connections.
  - `blink_task()`: Blinks the onboard LED to indicate connection status.
  - `main()`: Starts all tasks (button monitoring, BLE, and LED blinking) concurrently.
  - `begin()`: Initializes and runs the gamepad.

#### **3. `GamePadServer`**

Handles BLE communication for a central device connecting to the gamepad.

- **Attributes**:
  - `device_name`: The BLE device name to advertise.
  - `led`: Onboard LED for status indication.
  - `connected`: Tracks connection status.
  - `connection`: Active BLE connection.
  - `command`: Last received command from the gamepad.
  - `_REMOTE_UUID` and `_BUTTON_UUID`: UUIDs for BLE services/characteristics.

- **Methods**:
  - `peripheral_task()`: Manages BLE connection and disconnection.
  - `blink_task()`: Blinks the LED based on connection status.
  - `read_commands()`: Reads BLE notifications from the gamepad.
  - `find_remote()`: Scans for BLE devices matching the specified name.
  - `main()`: Runs tasks concurrently for BLE communication and command handling.

- **Properties**:
  Properties like `is_up`, `is_a`, etc., return `True` if the last received command corresponds to a specific button action.

---

### **Functions and Tasks**

1. **`monitor_buttons()`**
   - Polls the state of each button and updates the OLED/BLE.
   - Notifies button press/release events over BLE if connected.

2. **`peripheral_task()`**
   - Starts BLE advertising with the specified service UUID.
   - Handles BLE connections and updates the OLED display.

3. **`blink_task()`**
   - Toggles the LED at different intervals based on connection status.

4. **`find_remote()`**
   - Scans for BLE devices advertising the expected device name.

5. **`read_commands()`**
   - Reads and processes BLE notifications from the gamepad, updating the `command` attribute.

6. **`main()`**
   - Runs all asynchronous tasks (`peripheral_task`, `monitor_buttons`, etc.) concurrently.

---

### **Usage Flow**

1. Initialize the **`GamePad`** instance.
2. Call `begin()` to start all tasks:
   - Advertise BLE service.
   - Continuously monitor button states.
   - Blink the LED for status.
3. On a separate BLE central device, use **`GamePadServer`** to:
   - Connect to the gamepad.
   - Receive button press/release notifications.
   - Interpret commands with convenience properties (`is_a`, `is_up`, etc.).

---

### **BLE Communication**

- **Service UUID**: `0x1848`
- **Characteristic UUID**: `0x2A6E`
- **Commands**: Sent as strings (e.g., `a_down`, `up_down`).

---

### **Hardware Setup**

1. **Buttons**: Connect to GPIO pins defined in `GamePad.buttons`.
2. **OLED**: Connect via I2C (default SDA: 0, SCL: 1).
3. **LED**: Use onboard LED (`"LED"`).

---
