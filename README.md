# AstroGuard - MLOps para Detecção de Objetos Próximos da Terra (NEOs)

Projeto de MLOps para ingestão, classificação e monitoramento de objetos próximos da Terra (Near-Earth Objects), utilizando dados da NASA.

## 🔭 Objetivo
Detectar e classificar objetos próximos da Terra com base em dados orbitais e físicos, e disponibilizar uma API para inferência.

## 🧱 Estrutura do Projeto

- `data/`: Dados brutos e processados
- `src/`: Scripts de ingestão, pré-processamento, modelagem e deploy
- `models/`: Modelos treinados
- `notebooks/`: Prototipagem e visualização
- `pipelines/`: Definições de pipeline com DVC ou Airflow
- `tests/`: Testes unitários e de integração

## 🚀 Primeiros Passos

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure sua chave da API da NASA:
   ```bash
   export NASA_API_KEY=your_key
   ```

3. Execute o script de ingestão:
   ```bash
   python src/ingest/download_neo_data.py
   ```

## 📦 Requisitos
- Python 3.10+
- requests
- dvc (opcional)

## 📄 Licença
MIT
