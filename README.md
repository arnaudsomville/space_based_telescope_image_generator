# Installation

1. To setup the environnement, make sure to install miniconda https://docs.anaconda.com/miniconda/miniconda-install/
2. Create your python environnement
```
conda create -y -n my_env python=3.11
conda activate my_env
pip install pdm ruff=0.3.3 pre-commit
```
3. Go to your folder and install the packages using **pdm**. Initialize the project if needed
```
cd ~/your_work_folder
pdm install
```


### Steps to Set Up Documentation

1. **Activate the Conda Environment:**
   - Open a terminal in your project directory and activate the `my_env` environment:
     ```bash
     conda activate my_env
     ```

2. **Initialize Sphinx:**
   - Run the Sphinx setup command:
     ```bash
     sphinx-quickstart --no-sep --project="Your Project" --author="Your Name" --release="0.1" --quiet docs
     ```
3. **Customize `conf.py`:**
   - Open the `docs/conf.py` file to configure Sphinx.
   - You can customize it as much as you want but a template is provided and I STRONGLY recommend you to use it (modify it with your info)

4. **Generate Documentation:**
   - Copy the sources in the documentation using
     ```bash
     sphinx-apidoc -o docs/ src/ --force --separate
     ```
   - Build the documentation with:
     ```bash
     cd docs
     make html
     ```
   - The HTML files will be generated in the `docs/_build/html` directory.

5. **Preview the Documentation:**
   - Open the `index.html` file in a web browser:
     ```bash
     open docs/_build/html/index.html
     ```

### Customizing the Documentation

- **Add Content:**
  - Write your documentation in `.rst` files within the `docs/source` directory.
  - Update the `index.rst` file to include references to your new files.

- **Automate API Documentation:**
  - Use `sphinx.ext.autodoc` to automatically generate documentation from your Python code:
    ```bash
    sphinx-apidoc -o docs/ src/
    ```

With these steps, you can easily set up and manage your project documentation using Sphinx.

## Deploying Documentation to GitHub Pages

This project is set up to automatically generate and deploy Sphinx documentation to GitHub Pages using a GitHub Actions workflow. Follow these simple steps to enable deployment of your documentation:
