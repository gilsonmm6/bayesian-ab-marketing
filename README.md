# 🎯 Inferência Bayesiana Aplicada a A/B Testing de Marketing

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![PyMC](https://img.shields.io/badge/PyMC-5.x-purple)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completo-brightgreen)

## ⚠️ Nota sobre visualização dos notebooks

Os notebooks deste projeto utilizam **PyMC 5** para amostragem MCMC, que gera barras de progresso interativas via `ipywidgets` durante a execução no Google Colab. A partir de 2023, o Colab passou a injetar automaticamente metadados de widgets (`metadata.widgets`) nos arquivos `.ipynb` — metadados que o GitHub não consegue renderizar, exibindo a mensagem "Invalid Notebook".

**Os notebooks funcionam perfeitamente.** Para executá-los:

1. Acesse [Google Colab](https://colab.research.google.com/)
2. Clique em **Arquivo → Abrir notebook → GitHub**
3. Cole o link do repositório: `https://github.com/gilsonmm6/bayesian-ab-marketing`
4. Selecione o notebook desejado e execute

## 📌 Problema de negócio

Exibir anúncios pagos aumenta a taxa de conversão comparado a anúncios
de serviço público? Respondemos com **inferência bayesiana completa** —
não apenas "sim ou não", mas com quantificação de incerteza, critérios
de decisão práticos e otimização do tempo de experimento.

## 🔑 Resultados principais

| Métrica | Resultado |
|---|---|
| P(ad > psa) | **100.00%** |
| Lift médio | **+43.35%** |
| BF10 | **1.70 × 10²²⁰** (Decisivo) |
| ROPE | HDI completamente fora — efeito prático confirmado |
| Parada adaptativa | Decisão em n=15.000 (**97.4% de economia**) |
| Melhor dia | Segunda-feira (3.32% de conversão) |

## 🧠 Metodologia

Fase 1 → EDA + setup do ambiente

Fase 2 → Frequentista vs Bayesiano (Beta-Binomial, PyMC)

Fase 3 → ROPE + Bayes Factor + Parada Adaptativa + Hierárquico

Fase 4 → PPC + LOO-CV + Relatório executivo

## 🛠️ Stack

- **Modelagem:** PyMC 5, ArviZ
- **Análise:** pandas, NumPy, SciPy
- **Visualização:** matplotlib
- **Ambiente:** Google Colab / Jupyter

## ▶️ Como executar

```bash
pip install pymc>=5.0 arviz>=0.16 pandas matplotlib scipy
```

Execute os notebooks em ordem:
`00_setup` → `01_bayesian_ab_test` → `02_rope_bf_sequential` → `03_validation_storytelling`

Dataset: [Marketing A/B Testing — Kaggle](https://www.kaggle.com/datasets/faviovaz/marketing-ab-testing)

## 👤 Autor

**Gilson Machado Monteiro**  
Data Analyst & BI Analyst | Especialização em Estatística Aplicada (PUC Minas)  
[LinkedIn](https://linkedin.com/in/gilsonmm6) · [GitHub](https://github.com/gilsonmm6)
