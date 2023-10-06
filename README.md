# Intelli-Service
### Description
The project aims to create a comprehensive platform tailored to the needs of undergraduate students who require academic assistance. Among the various services offered, a key feature will be an AI-powered service designed to deliver top-notch educational content. Students can request content on specific subjects, specifying their preferred tutor. The system will generate personalized video content, presenting the requested topic in the distinctive style of the chosen professor.

# Project Directory Structure:

This is a simplified representation of a project directory structure for a data science project.

- **Intelli-Service/**: The main project directory.

  - **data/**: Directory for data storage.
    - **raw/**: Original, unprocessed data files, A.K.A ingested data.
      - `dataset1.csv`
      - `dataset2.xlsx`
    - **processed/**: Cleaned and preprocessed data files.
      - `clean_data.csv`
      - `transformed_data.pkl`
    - **external/**: Data from external sources.
      - `external_data.csv`
      - `geospatial_data.geojson`
    - **intermediate/**: Intermediate data files.
      - `wrangled_data.csv`
      - `ingested_data.json`

  - **notebooks/**: Jupyter notebooks for different stages of the project.
    - `exploratory_analysis.ipynb`
    - `data_wrangling.ipynb`
    - `data_preparation.ipynb`
    - `model_training.ipynb`

  - **src/**: Python source code for the project.
    - **data/**: Code for data-related tasks.
      - `data_loader.py`
      - `data_preprocessing.py`
      - `data_wrangling.py`
      - `feature_engineering.py`
    - **models/**: Code for defining and training machine learning models.
      - `model.py`
      - `evaluation.py`
    - **deployment/**: Code for deployment.
      - `app.py`
      - `deployment_utils.py`
      - `requirements.txt`
    - **visualization/**: Code for creating data visualizations and plots.
      - `plot_utils.py`
      - `visualize_results.py`
    - **utils/**: Utility functions and configuration settings.
      - `config.py`
      - `logging_config.py`
      - `helper_functions.py`

  - **tests/**: Testing scripts and files for different project components.
    - `test_data.py`
    - `test_models.py`
    - `test_utils.py`
  - **reports/**: Project-related reports and presentations.
    - `project_report.pdf`
    - `presentation.pptx`

- `requirements.txt`: List of Python packages and dependencies.
- `README.md`: Project overview and instructions.
- `LICENSE`: Project license information.

### Description

- **data/**: This directory contains data files. It includes raw data, processed data, external data, and intermediate data.
- **notebooks/**: Jupyter notebooks for different stages of the project, such as data exploration, data wrangling, data preparation, and model training.
- **src/**: Python source code for the project, organized into subdirectories for data, models, deployment, visualization, and utilities.
- **tests/**: Testing scripts and files for different project components.
- **reports/**: Project-related reports, documentation, or presentations.
- **requirements.txt**: A list of Python packages and dependencies.
- **README.md**: Project overview and instructions.
- **LICENSE**: The project's license information.


## Project Creation with Miniconda or Anaconda:

**Download Miniconda or Anaconda**:
   Visit the [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution) website and download the installer for your operating system (e.g., Windows, macOS, Linux). Choose the Python 3.x version.


### Managing `requirements.txt` in a Python Project

This guide provides steps for dealing with the `requirements.txt` file in your Python project, including its creation and updates.

1. **Create a Virtual Environment:**
   Before starting your project, consider creating a virtual environment to isolate dependencies:

   ```bash
   conda create --name myenv /path/to/requirements.txt
   ```
   Make sure to replace /path/to/requirements.txt with the actual path to your requirements.txt file.
2. **Activate the Conda Environment:**
    Activate the environment using the following command:
    ```bash
    conda activate myenv
    ```
3. **Verify Environment Creation:**
    You can verify that the environment has been created and that the packages specified in requirements.txt have been installed:
    ``` bash
    conda list
    ```
4. **Update Dependencies:**
    Whenever you install any packages using `pip` or `conda` 
    make sure to update `requirements.txt` file using:
    ```bash
    pip freeze > requirements.txt
    ```
    And commit the changes to `Github`
5. **Update existed env:**
    If you already have created the enviroment and need to update it from the `requirements.txt` file using this command:
    ```bash
    conda install --file path/to/requirements.txt
    ```
6. **Deactivate the Envirement:**
    deactivate the env when you're done:
    ```bash 
    conda deactiavte
    ```
