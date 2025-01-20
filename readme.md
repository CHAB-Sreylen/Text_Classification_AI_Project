## Getting Start

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.x
*   pip (Python package installer)

### Installation

1.  **Create a virtual environment:**

    ```bash
    python -m venv .venv
    ```

    This creates an isolated Python environment for your project dependencies.

2.  **Activate the virtual environment:**

    *   **Windows:**

        ```bash
        .venv\Scripts\activate
        ```

    *   **Linux/macOS:**

        ```bash
        source .venv/bin/activate
        ```

3.  **Install required libraries:**

    ```bash
    pip install -r requirements.txt
    ```

    This installs the necessary Python packages listed in the `requirements.txt` file. Make sure this file exists in your project's root directory.

4.  **Configure Model Path:**

    This step is necessary if your application uses a model file.

    *   Locate the model file within the `model` folder (or wherever your models are stored).
    *   Right-click on the model file and copy its full path.
    *   Open the `app.py` file (or your main application file).
    *   Find the line of code where the model path is defined (e.g., `model_path = "path/to/your/model.pkl"`).
    *   Replace the existing path with the copied path. Example: `model_path = "C:/Users/YourName/path/to/your/model.pkl"` (Windows) or `/home/yourname/path/to/your/model.pkl` (Linux/macOS).

5.  **Run the Flask application:**

    ```bash
    flask run
    ```

    This command starts the Flask development server. You should see output indicating the server is running, usually at `http://127.0.0.1:5000/` or `http://localhost:5000/`.
