# FileSorter


### Table of Contents
----
1. [Project Overview](#projectoverview)
	- [Technologies Used](#keytechnologies)
2. [Getting Started](#gettingstarted)
	- [Prerequisites](#prerequisites)
	- [Installation](#installation)
	- [Parameters](#parameters)
3. [Contact](#contact)

### <a name="projectoverview"></a>Project Overview
----
This project consists of a tool able to organize your files based on context similarity, grouping them in folders with the context as name.  

*Note: This project currently sorts only PDFs*  
#### <a name="keytechnologies"></a>Technologies Used
- Ollama 0.5.5  
- Python 3.12.2  

### <a name="gettingstarted"></a>Getting Started
---
#### <a name="prerequisites"></a>Prerequisites

To be able to run the project, make sure to have the following tools installed:  

- **Ollama**:  
	Go to https://ollama.com/download and select your platform 
	*Note: This project is currently only available for Windows*  
- **AI model of preference** (*gemma:2b by default*):  
	By default, it will automatically pull the model on the first run. Otherwise execute ```ollama run gemma:2b``` or any other AI model for the first time to pull from the repository the corresponding model.  

#### <a name="installation"></a>Installation

1.  Clone the repository:  
	```
	git clone https://github.com/Terzer-bit/FileSorter.git
	```  
2. Change directory to the project folder:  
	`` cd FileSorter `` *for PowerShell*  
	`` chdir FileSorter `` *for cmd*  
3. Install the requirements:  
	```
	pip install -r requirements.txt
	```  
4. Execute the script file:  
	```
	pyhton ./FileSorter.py
	```  

#### <a name="parameters"></a>Parameters

*Parameters are displayed at the beginning of the code*

- **modelToUse**: The model's name in Ollama (*gemma:2b by default*).
- **enableManualPath**: Bool that allows switching between asking the user what path wants to insert and automatically sorting the file specified in **folderPath** (*False by default*).
- **folderPath**: The file to sort when **enableManualPath** is set to False (*default*).

### <a name="contact"></a>Contact
---
For any details contact the owner of the project on:
- Email: garciavinapablo@gmail.com
- LinkedIn: [pablo-garcía-viña](https://www.linkedin.com/in/pablo-garc%C3%ADa-vi%C3%B1a/)
