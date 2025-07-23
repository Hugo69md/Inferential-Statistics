# Inferential Statistics Project

A comprehensive Python project for statistical analysis and hypothesis testing, featuring various statistical tests and data analysis tools.

## 📊 Data Sources / filtering 

This script only handles CSV but you can modify it to access .parquet or any other extension, in the analysis.py file

To change to dataset to analyse : 
- put your CSV file in the root of your project
- go to utils > analysis > analysis.py
- change the name in brackets in LINE 6, to match your file to analyse 

Your data will now be the source of future analysis !

To apply filters to you dataset :
- go to utils > filtering > dfmodif.py
- using pandas, you can apply filters to your data, small examples are available in the provided dfmodif file

Your data is now filtered ! enjoy your analysis !

## 📦 Required Libraries

Before running this project, ensure you have the following Python libraries installed:

- **pandas** - Data manipulation and analysis
- **seaborn** - Statistical data visualization
- **matplotlib** - Plotting and visualization
- **numpy** - Numerical computing
- **scipy** - For hypothesis testing and other stat tests
- **os** - For file directions for outputs
- **datetime** - For labelling when the test have been done

### Installation

You can install all required dependencies using pip:

```bash
pip install pandas seaborn matplotlib scipy numpy scipy os datetime
```

Or if you're using a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pandas seaborn matplotlib scipy numpy scipy os datetime
```

## 🚀 How to Run

To execute the main program, Make sure you're in the project root directory when running this command.

```bash
python3 main.py
```
let the console guide you into what you want to do with the script !

## 📁 Project Structure

This project contains various statistical analysis tools organized in the following structure:

- `utils/` - Utility functions for analysis, data selection, filtering, and tool choice
- `tools/` - Statistical testing tools including hypothesis testing and distribution tests
- `hypothesis_testing/` - Comprehensive hypothesis testing modules
  - Distribution tests (normality, skewness, etc.)
  - Parametric and non-parametric tests
  - One-sample and two-sample tests
- `outputs/` - All the outputs are here ! 

## 🔬 Features

- **Hypothesis Testing**: Comprehensive statistical hypothesis testing tools
- **Distribution Analysis**: Normality tests, skewness analysis, and more
- **Data Filtering**: Advanced data selection and filtering capabilities
- **Statistical Visualization**: Integrated plotting and visualization tools
- **Parametric & Non-parametric Tests**: Support for various statistical test types

## 📋 Requirements

- Python 3.x
- Required libraries (see above)
- Sufficient system memory for data processing

## 🤝 Contributing

I will not accept any push request but it is open source, you can modify it as it pleases you !

## 📄 License

This project is open source and available under standard licensing terms.
