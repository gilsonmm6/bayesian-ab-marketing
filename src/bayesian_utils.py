"""
bayesian_utils.py
Funções utilitárias reutilizáveis — Inferência Bayesiana Aplicada
Projeto: bayesian-ab-marketing
Autor: Gilson Machado Monteiro
"""

import numpy as np
import arviz as az
from scipy import stats as scipy_stats
from scipy.stats import gaussian_kde


def summarize_posterior(trace, var_names, hdi_prob=0.95):
    """
    Resumo do posterior para um conjunto de variáveis.
    Retorna média, desvio padrão, HDI, R-hat e ESS.
    """
    print(f"RESUMO POSTERIOR (HDI {hdi_prob:.0%})")
    print("─" * 55)
    for var in var_names:
        mean  = float(trace.posterior[var].mean())
        std   = float(trace.posterior[var].std())
        hdi   = az.hdi(trace, var_names=[var], hdi_prob=hdi_prob)[var].values
        rhat  = float(az.rhat(trace)[var])
        ess   = float(az.ess(trace)[var])
        ok_r  = "✓" if rhat < 1.01 else "✗"
        ok_e  = "✓" if ess  > 400  else "✗"
        print(f"  {var:<14} mean={mean:.6f}  std={std:.6f}")
        print(f"  {'':14} HDI=[{hdi[0]:.6f}, {hdi[1]:.6f}]")
        print(f"  {'':14} R-hat={rhat:.4f}{ok_r}  ESS={ess:.0f}{ok_e}")
        print()


def rope_analysis(samples, rope_width, hdi_prob=0.95):
    """
    Análise ROPE para amostras do posterior de delta.
    Retorna decisão, P(dentro ROPE) e P(fora ROPE).
    """
    hdi = az.hdi(np.array(samples), hdi_prob=hdi_prob)
    rope_low, rope_high = -rope_width, +rope_width

    p_dentro = ((np.array(samples) >= rope_low) &
                (np.array(samples) <= rope_high)).mean()
    p_fora   = 1 - p_dentro

    hdi_fora = hdi[0] > rope_high or hdi[1] < rope_low
    hdi_dent = hdi[0] >= rope_low  and hdi[1] <= rope_high

    if hdi_fora:
        decisao = "IMPLANTAR — HDI completamente fora do ROPE"
    elif hdi_dent:
        decisao = "NÃO IMPLANTAR — HDI completamente dentro do ROPE"
    else:
        decisao = "INCONCLUSIVO — HDI sobrepõe parcialmente o ROPE"

    return {
        "rope":     (rope_low, rope_high),
        "hdi":      (hdi[0], hdi[1]),
        "p_dentro": p_dentro,
        "p_fora":   p_fora,
        "decisao":  decisao,
    }


def bayes_factor_savage_dickey(posterior_samples, prior_a, prior_b, n_prior=100_000):
    """
    Calcula BF10 via método Savage-Dickey.
    Compara H1 (delta != 0) vs H0 (delta = 0).
    """
    prior_ad  = scipy_stats.beta.rvs(prior_a, prior_b, size=n_prior)
    prior_psa = scipy_stats.beta.rvs(prior_a, prior_b, size=n_prior)
    prior_delta = prior_ad - prior_psa

    kde_prior     = gaussian_kde(prior_delta)
    kde_posterior = gaussian_kde(posterior_samples)

    prior_at_0     = kde_prior(0)[0]
    posterior_at_0 = kde_posterior(0)[0]

    BF10 = prior_at_0 / posterior_at_0 if posterior_at_0 > 0 else np.inf

    if BF10 == np.inf or BF10 > 100:
        classificacao = "Decisiva"
    elif BF10 > 30:
        classificacao = "Muito forte"
    elif BF10 > 10:
        classificacao = "Forte"
    elif BF10 > 3:
        classificacao = "Moderada"
    elif BF10 > 1:
        classificacao = "Anedótica"
    else:
        classificacao = "Favorece H0"

    return {"BF10": BF10, "classificacao": classificacao}


def adaptive_stopping(df, group_col, outcome_col, prior_a=2, prior_b=98,
                      p_threshold=0.95, hdi_threshold=0.005, step=5000):
    """
    Simula critério de parada adaptativa bayesiana.
    Retorna histórico e ponto de decisão.
    """
    df_sorted = df.sort_values(group_col).reset_index(drop=True)
    N_MAX     = len(df_sorted)
    historico = []
    decisao   = None

    for n in range(step, N_MAX + step, step):
        subset = df_sorted.iloc[:n]
        n_a = int((subset[group_col] == "ad").sum())
        n_p = int((subset[group_col] == "psa").sum())
        c_a = int(subset[subset[group_col] == "ad"][outcome_col].sum())
        c_p = int(subset[subset[group_col] == "psa"][outcome_col].sum())

        if n_a == 0 or n_p == 0:
            continue

        s_a = scipy_stats.beta.rvs(prior_a + c_a, prior_b + n_a - c_a, size=5000)
        s_p = scipy_stats.beta.rvs(prior_a + c_p, prior_b + n_p - c_p, size=5000)
        d   = s_a - s_p

        p_melhor = (d > 0).mean()
        hdi_w    = np.percentile(d, 97.5) - np.percentile(d, 2.5)

        historico.append({"n": n, "p_melhor": p_melhor, "hdi_width": hdi_w})

        if decisao is None:
            if p_melhor > p_threshold:
                decisao = {"n": n, "acao": "IMPLANTAR ad", "p_melhor": p_melhor}
            elif p_melhor < 1 - p_threshold:
                decisao = {"n": n, "acao": "MANTER psa",   "p_melhor": p_melhor}
            elif hdi_w < hdi_threshold:
                decisao = {"n": n, "acao": "PARAR por precisão HDI", "p_melhor": p_melhor}

    return historico, decisao
