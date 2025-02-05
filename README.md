# Smart Walking Stick 🦯

A Raspberry Pi-powered smart walking stick system designed to enhance mobility and independence for visually impaired users through advanced navigation assistance, obstacle detection, and emergency alert features.

<p align="center">
  <a href="#features">Features</a> •
  <a href="#requirements">Requirements</a> •
  <a href="#setup">Setup</a> •
  <a href="#usage">Usage</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

## ✨ Features

### 🔍 Core Features
- **Obstacle Detection**
  - Real-time detection of obstacles within 30cm range
  - Dual ultrasonic sensor system for reliability
  - Immediate audio feedback

- **Navigation System**
  - Turn-by-turn voice navigation
  - Real-time GPS tracking
  - Distance and ETA calculations

- **Emergency System**
  - One-touch emergency activation
  - Automated email alerts
  - SMS notifications via Fast2SMS
  - Location sharing

### 🎯 Smart Features
- **Voice-Activated Services**
  - Real-time weather updates
  - Latest news headlines
  - Location announcements
  - Time updates
  - Nearby places discovery

- **Safety Features**
  - Traffic signal detection
  - Continuous distance monitoring
  - Voice feedback system

## 🛠 Requirements

### Hardware
- Raspberry Pi (3 or newer recommended)
- HC-SR04 Ultrasonic Sensors (x2)
- GPS Module
- Pi Camera Module
- Push Button
- Speaker/Headphone Output
- Microphone Input

### Software Dependencies
```bash
pip install -r requirements.txt
```

### API Requirements
You'll need API keys for:
- Google Maps API
- NewsAPI
- OpenWeatherMap
- Fast2SMS
- AssemblyAI

## 🚀 Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/JJbuc/Smart-Walking-Stick.git
   cd Smart-Walking-Stick
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**
   - Create a `.env` file in the root directory
   ```env
   GOOGLE_MAPS_API_KEY=your_key_here
   NEWS_API_KEY=your_key_here
   WEATHER_API_KEY=your_key_here
   FAST2SMS_API_KEY=your_key_here
   ASSEMBLY_AI_KEY=your_key_here
   ```

4. **Hardware Setup**
   - Connect the ultrasonic sensors to GPIO pins:
     - Sensor 1: TRIGGER=21, ECHO=20
     - Sensor 2: TRIGGER=23, ECHO=24
   - Connect the push button to GPIO 12
   - Ensure GPS module is connected to serial port
   - Connect audio input/output devices

5. **Run the System**
   ```bash
   python main.py
   ```

## 📖 Usage

### Voice Commands
Press the button and use any of these commands:
- "Navigate to [destination]"
- "What's the weather?"
- "Where am I?"
- "What's the news?"
- "Find nearby places"
- "What time is it?"
- "Emergency"

### File Structure
```
smart-walking-stick/
├── main.py           # Main application entry
├── features.py       # Core features implementation
├── drivers.py        # Hardware interfaces
├── ultrasonic.py    # Sensor control
├── gps.py           # GPS interface
├── red_color.py     # Traffic signal detection
├── send_message.py  # Emergency alerts
└── nearByPlaces.py  # Location services
```

## Paper Link
[https://ieeexplore.ieee.org/abstract/document/10180466](url)
