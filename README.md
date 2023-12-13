<h1 align="center"> Clasificación de la producción de Dark Photons en el experimento ATLAS utilizando machine learning.  </h1>

Este repositorio contiene el trabajo de tésis de pregrado, donde se buscan encontrar modelos de ML que permitan separar VBF de ggF sin aplicar cortes restrictivos.  

## Archivos 
[analisis.ipynb](analisis.py) contiene la separación de VBF con respecto de ggF aplicando los cortes tradicionales. Estos son MET > 225 GeV y mjj > 1 TeV  
[ml.ipynb](ml.ipynb) contiene el trabajo de ML donde se aplica XGBOOST Classifer para separar ggF de VBF.