# 🎥 2D & 3D Visual Animation using OpenGL in Python

This project showcases **interactive 2D and 3D visual animations** using **OpenGL** in Python. Designed as a learning and experimentation platform, it demonstrates real-time rendering, object transformations, and basic animation techniques using PyOpenGL and related libraries.

---

## ✨ Project Overview

The goal of this project is to explore and implement:

- Real-time rendering of **2D and 3D objects**
- **Transformations** such as rotation, translation, and scaling
- **Camera manipulation** and projection techniques
- Basic **lighting and shading models**
- Simple **animation loops** and object interactions

The project is modular, making it easy to expand into simulations, games, or educational visualizations.

---

## 🛠️ Technologies Used

- **Python 3.8+**
- **PyOpenGL** – OpenGL bindings for Python
- **GLUT / GLFW** – Windowing and input handling
- **NumPy** – For efficient numerical operations
- **PyGame (optional)** – For event handling and sound integration

---

## 🧩 Key Features

- 📐 **2D Drawing**: Shapes, lines, and animations in a 2D context  
- 🧊 **3D Object Rendering**: Cubes, spheres, pyramids, etc.  
- 🔁 **Real-time Animation**: Frame-based object movement  
- 🎥 **Camera Controls**: Basic navigation and perspective manipulation  
- 💡 **Lighting Effects**: Directional and ambient light (optional extensions)  
- 🎮 **User Interaction**: Keyboard/mouse-based input



## 📂 Project Structure

```bash
.
├── main.py                # Entry point: initializes OpenGL and rendering loop
├── shapes/                # Custom 2D and 3D shape definitions
│   ├── cube.py
│   ├── sphere.py
│   └── ...
├── utils/                 # Transformation matrices, lighting helpers
├── assets/                # Optional textures, shaders, or models
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies




## 🧪 Getting Started
1. Clone the Repository
git clone https://github.com/your-username/visual-animation-opengl.git
cd visual-animation-opengl

2. Set Up Virtual Environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt


Make sure your system supports OpenGL and necessary drivers are installed.

## ▶️ Running the Project
python main.py


The OpenGL window will launch with the selected animation.

## 💡 Use Cases

🎓 Educational demos for computer graphics students
🎮 Game prototype development
🔬 Simulations and physics-based visualizations
🧪 Experimental graphics algorithms

## 📌 Requirements

Python 3.8 or higher
A GPU with OpenGL 2.0+ support
Optional: GLFW or PyGame for advanced window/input management

## 🚀 Future Enhancements

🌈 Add texture mapping and materials
🌍 Import 3D models (e.g., .obj files)
📷 Implement FPS-style camera controls
🌐 GUI overlay for parameter controls
💥 Particle systems or physics engine integration

## 📄 License

This project is open-source and free to use under the MIT License.
---
