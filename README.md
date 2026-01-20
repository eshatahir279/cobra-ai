#  Cobra AI // Cinematic Studio

Cobra AI is a professional-grade desktop interface for generating high-fidelity artwork using the Stable Diffusion XL (SDXL) engine. Built with a focus on minimalist UX, it features a ChatGPT-inspired conversational flow and a "Glassmorphic" design aesthetic.



##  Key Features
* **Conversational UI:** High-speed, threaded chat interface to track your creative history.
* **Cinematic Watermark:** A sleek "Imagine & Generate" landing state for a clean workspace.
* **Multi-Threaded Performance:** Image generation happens in the background to prevent GUI freezing.
* **Secure Key Management:** Full `.env` integration to keep API credentials safe.
* **Modern Iconography:** Minimalist vector-style controls for a 2026-standard look.

##  Technical Stack
* **Language:** Python 3.10+
* **GUI Framework:** CustomTkinter (Modernized Tkinter)
* **AI Engine:** Stability AI (SDXL 1.0)
* **Networking:** Requests & Threading for asynchronous API calls
* **Image Processing:** Pillow (PIL)

##  Getting Started

### Prerequisites
1. Get a free API Key from [Stability AI](https://platform.stability.ai/).
2. Install the required Python libraries:
   ```bash
   pip install customtkinter requests pillow python-dotenv
