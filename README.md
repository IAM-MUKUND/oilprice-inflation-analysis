# Does Crude Oil Price Volatility Affect Inflation in India?

## Econometric Analysis --- Research Log

**Status:** Analysis documented; final specification selected; report-ready with limitations disclosed
**Software:** Gretl 2026c-git
**Frequency:** Monthly
**Merged data:** January 2013--December 2025
**Descriptive sample:** January 2014--December 2025 (144 observations)
**Final dynamic-regression sample:** January 2015--December 2025 (132 observations)

## 1. Research question

This project investigates whether crude oil price movements are
associated with consumer inflation in India, while considering changes
in the INR/USD exchange rate. The regressions are exploratory and do not
establish causation.

## 2. Data sources and variables

Sources used during preparation: - **Crude oil:** PPAC Indian Basket
crude oil historical data. - **CPI:** RBI DBIE Combined General Consumer
Price Index and Combined Inflation (%). - **Exchange rate:** RBI
monthly-average INR per US dollar series; monthly average, not end-month
rate.

The extracted CPI inflation series is unavailable for 2013, so the main
analysis starts in January 2014. The data extraction and source
alignment should still be checked before final submission. In
particular, verify the unusually sharp CPI decline at the end of 2025
against the original RBI source and metadata; do not remove it without
evidence.

---

  Variable                            Meaning

---

  `cpi_inflation_yoy_pct`             Combined CPI year-on-year
                                      inflation, percent

  `cpi_combined_index`                Combined CPI index, base 2012 = 100

  `oil_price_usd_bbl`                 Indian Basket crude oil price,
                                      USD/barrel

  `oil_change_pct`                    Month-to-month percentage change in
                                      oil price

  `oil_log_return_pct`                Month-to-month log change in oil
                                      price, multiplied by 100

  `oil_volatility_3m`                 Rolling three-month sample standard
                                      deviation of oil log returns

  `usd_inr_monthly_avg`               Monthly average INR per USD

`usd_inr_change_pct`                Month-to-month percentage change in
                                      INR per USD
-------------------------------------------------

Definitions: - Oil percentage change =
`100 × (P_t − P_(t−1)) / P_(t−1)` - Oil log return =
`100 × (ln(P_t) − ln(P_(t−1)))` - Three-month volatility = rolling
sample standard deviation of the current and previous two oil log
returns. - INR/USD percentage change =
`100 × (FX_t − FX_(t−1)) / FX_(t−1)`. A positive value indicates rupee
depreciation.

## 3. Descriptive statistics

For the 144-observation sample:

---

  Variable               Mean       Median      Minimum      Maximum         Std.
                                                                        deviation

---

  CPI inflation        4.9072       5.0050         0.25         8.60       1.6994
  (%)

  Oil price            68.277       67.007       19.902       116.01       19.869
  (USD/barrel)

  INR per USD          73.030       72.035       59.305       90.091       8.2644

  Oil price            0.1992       0.7839      −40.340       53.784       10.731
  change (%)

  Oil log return      −0.3878       0.7808      −51.652       43.038       11.026
  (%)

  Three-month          7.3262       5.6710       0.4631       54.009        7.105
  oil volatility
  (%)

INR/USD change       0.2674       0.2356      −2.4475       4.0037       1.1529
  (%)
-----

Oil changes and log returns are highly correlated (about 0.989), so they
should generally not both be included in the same small model without a
clear reason.

Correlations with CPI inflation: - Oil price level: +0.3127 - INR/USD
level: −0.1442 - Oil percentage change: +0.0492 - Oil log return:
+0.0280 - Three-month oil volatility: +0.0983 - INR/USD percentage
change: −0.0122

These are descriptive correlations, not causal estimates. Time-series
persistence and trends can make simple correlations misleading.

## 4. Initial plot observations

- Oil prices fell sharply in 2015--2016 and around 2020, then
  recovered and rose around 2022.
- CPI inflation varies over the sample, with a pronounced decline at
  the end of 2025 that requires source verification.
- INR per USD generally trends upward, consistent with long-run rupee
  depreciation.

These are descriptive observations only.

## 5. Unit-root tests completed

ADF tests used Gretl. `--c` includes a constant; `--ct` includes a
constant and linear trend. Lag selection affects results, so the
analysis does not select a specification merely because it gives a
preferred p-value.

### CPI inflation

With a constant and 2, 3, 6 and 12 lagged differences, the unit-root
null was not rejected at 5%. At six lags, p ≈ 0.0969 (marginal at 10%);
at 12 lags, p ≈ 0.4832. Evidence is inconclusive under the tested
specifications.

### Oil price level

With constant and trend:

      Lagged differences   ADF statistic   p-value

---

                       2        −3.01695    0.1274
                       3        −3.06798    0.1140
                       6        −3.43592   0.04668
                      12        −2.31524    0.4250
    AIC-selected lag (1)             ---   0.08965

Results are sensitive to lag choice; the oil-price level should not be
declared stationary based only on the six-lag result.

### INR/USD level

ADF tests with constant and trend did not reject the unit-root null in
the tested specifications. An AIC-selected one-lag test had p ≈ 0.1921.

### Oil log returns and INR/USD changes

At six lagged differences with a constant: - Oil log returns: statistic
−4.36477, p = 0.0003373. - INR/USD percentage changes: statistic
−4.44163, p = 0.0002452.

These reject the unit-root null under those specifications.

**Caveat:** COVID-19, the 2014--2016 oil decline and the 2022 shock may
involve structural changes that affect standard ADF tests. These are
preliminary diagnostics, not a complete stationarity analysis.

## 6. Model 1 --- baseline OLS

Gretl command:

```gretl
ols cpi_inflation_yoy_pct const oil_change_pct usd_inr_change_pct
series baseline_residuals = $uhat
series baseline_fitted = $yhat
modtest 12 --autocorr
```

Sample: January 2014--December 2025, T = 144.

  Variable             Coefficient   Std. error   p-value

---

  Constant                 4.90694     0.146516   \<0.001
  Oil price change        0.007698     0.013547    0.5707
  INR/USD change         −0.004925     0.126088    0.9689

Model statistics: - R² = 0.002433; adjusted R² = −0.011717 - F(2,141) =
0.171963; p = 0.842186 - Residual standard error = 1.709302 -
Durbin--Watson = 0.202465; Gretl `rho` = 0.894002

Neither predictor was statistically significant. The model explained
about 0.24% of CPI-inflation variation and was not significant overall.
The low Durbin--Watson statistic suggested strong positive residual
autocorrelation.

### Model 1 autocorrelation test

  Test                     Statistic        p-value

---

  Breusch--Godfrey LMF       43.3864   2.04 × 10⁻³⁹
  Breusch--Godfrey TR²      115.4056   5.07 × 10⁻¹⁹
  Ljung--Box Q′               344.04   2.54 × 10⁻⁶⁶

All tests reject the null of no residual autocorrelation through order
12. Conventional OLS inference is questionable under this residual
pattern.

## 7. Model 2 --- add inflation persistence

Gretl command:

```gretl
ols cpi_inflation_yoy_pct const cpi_inflation_yoy_pct(-1) oil_change_pct usd_inr_change_pct
series model2_residuals = $uhat
series model2_fitted = $yhat
modtest 12 --autocorr
```

Sample: February 2014--December 2025, T = 143.

  Variable                           Coefficient   Std. error        p-value

---

  Constant                              0.459287     0.193762         0.0191
  Previous month's CPI inflation        0.899141     0.037208   1.28 × 10⁻⁵¹
  Oil price change                     −0.002264     0.005899         0.7017
  INR/USD change                       −0.045513     0.054761         0.4073

Model statistics: - R² = 0.808320; adjusted R² = 0.804183 - F(3,139) =
195.3893; p = 1.17 × 10⁻⁴⁹ - Residual standard error = 0.741984 - Gretl
`rho` = 0.205130; Durbin's h = 2.739060

Adding lagged inflation substantially improved in-sample fit. The lagged
inflation coefficient is positive and highly significant, indicating
strong persistence. Oil changes and INR/USD changes remain statistically
insignificant. Their negative/positive signs should not be interpreted
as causal effects.

### Model 2 autocorrelation test

  Test                     Statistic       p-value

---

  Breusch--Godfrey LMF        5.5290   1.54 × 10⁻⁷
  Breusch--Godfrey TR²       49.0708   2.03 × 10⁻⁶
  Ljung--Box Q′              67.1685   1.08 × 10⁻⁹

All tests reject the null of no residual autocorrelation through order
12. Diagnostics improved relative to Model 1, but significant
autocorrelation remains. The high R² does not by itself establish model
adequacy.

## 8. Step 9 --- ADF test on Model 2 residuals

Gretl command:

```gretl
adf 6 model2_residuals --c
```

Results: - ADF statistic = −4.11023 - Asymptotic p-value = 0.0009314 -
Six lagged differences; sample size = 136 - First-order autocorrelation
estimate for ADF equation errors = −0.009 - Lagged differences joint
test: F(6,128) = 2.177, p = 0.0493

The ordinary ADF test rejects the unit-root null for the residual series
under this specification.

**Important qualification:** the ordinary ADF p-value on estimated
regression residuals is not a formal cointegration test using
residual-based critical values. Also, residual stationarity does not
remove the significant autocorrelation found by the Breusch--Godfrey
test; these diagnostics examine different properties.

## 9. Findings so far

1. Inflation is strongly persistent in Model 2.
2. Contemporaneous monthly oil-price changes are statistically
   insignificant in Models 1 and 2.
3. Contemporaneous INR/USD changes are statistically insignificant in
   Models 1 and 2.
4. Model 2 fits the sample far better than Model 1, but significant
   residual autocorrelation remains.
5. ADF evidence for CPI inflation and the oil-price level is sensitive
   to specification and lag order.
6. No causal conclusion has been established.

These are preliminary findings, not the final answer to the research
question.

## 10. Next steps

The immediate next stage should be a focused dynamic-specification check
rather than more arbitrary ADF lag testing:

1. Verify the source values and metadata for the sharp CPI decline at
   the end of 2025.
2. Inspect Model 2 residual ACF/PACF to understand the remaining serial
   pattern.
3. Test a small number of theoretically motivated specifications, such
   as lagged oil-price changes or the pre-defined oil-volatility
   measure. Keep the model parsimonious.
4. Re-run residual diagnostics after each meaningful specification
   change. Do not select a model solely because it raises R² or gives a
   preferred p-value.
5. Consider HAC/Newey--West standard errors for inference after
   clarifying the model. These can help account for heteroskedasticity
   and autocorrelation in standard errors, but do not repair a
   misspecified dynamic model.
6. Revisit stationarity and structural breaks for the final
   specification. Do not infer cointegration from the ordinary residual
   ADF p-value above.

**Status update:** these initial next steps were superseded by the focused dynamic-specification checks documented in Sections 12–15 below. The final model and remaining limitations are now recorded.

## 11. Reporting guidance

Separate the final write-up into: - **Results:** estimates, p-values,
test statistics, sample sizes and data sources. - **Interpretation:**
what the estimates suggest under the chosen specification. -
**Limitations:** serial correlation, lag sensitivity, possible
structural breaks, source-data checks and the distinction between
association and causation.

Do not write that an insignificant coefficient proves "no effect."
Prefer: "The estimated contemporaneous coefficient was not statistically
significant in this specification."

## 12. Focused dynamic specifications

After the initial models, the analysis moved from contemporaneous oil-price changes to a pre-defined three-month rolling oil-volatility measure. The aim was to test whether oil-market uncertainty might be associated with inflation after a short delay, while controlling for inflation persistence and monthly exchange-rate changes.

The specifications considered were:

- **Model 3:** add the second monthly lag of CPI inflation to Model 2.
- **Model 4:** add the 12-month lag of CPI inflation and retain contemporaneous oil-price changes.
- **Model 5:** replace contemporaneous oil-price changes with current three-month oil volatility.
- **Model 6:** use one-month-lagged three-month oil volatility, with CPI inflation lags 1, 2 and 12 and the monthly INR/USD percentage change.

The point of these comparisons was not to maximize \(R^2\) or search for a preferred p-value. The final specification was chosen to represent inflation persistence and a plausible delayed relationship with oil volatility.

### Model comparison summary

| Model | Main specification change                   | Sample | \(R^2\) |      AIC | Main result                                                         |
| ----- | ------------------------------------------- | -----: | ------: | -------: | ------------------------------------------------------------------- |
| 1     | Oil-price change + INR/USD change           |    144 |  0.0024 |       — | Neither predictor significant; severe residual autocorrelation      |
| 2     | Add CPI inflation lag 1                     |    143 |  0.8083 |       — | Inflation lag highly significant; oil and FX changes insignificant  |
| 3     | Add CPI inflation lag 2                     |    142 |  0.8138 |       — | Inflation lags important; oil and FX changes remain insignificant   |
| 4     | Add CPI inflation lag 12                    |   132* |  0.8109 | 289.0799 | Oil-price change remains insignificant                              |
| 5     | Current three-month oil volatility          |   132* |  0.8103 | 289.5357 | Current volatility insignificant (\(p=0.8003\))                     |
| 6     | One-month-lagged three-month oil volatility |    132 |  0.8144 | 286.5968 | Lagged volatility positive and significant with HAC standard errors |

\*The exact effective sample depends on the included lags and variable availability. Model 6's reported sample is January 2015–December 2025, \(T=132\).

The information criteria are directly comparable only when models use the same dependent variable and estimation sample. Treat the table as a summary of the analysis sequence, not as proof that one model is universally best.

## 13. Final specification — Model 6

### Gretl command

```gretl
set hac_kernel bartlett
set hac_lag 4
set hac_prewhiten off

ols cpi_inflation_yoy_pct const cpi_inflation_yoy_pct(-1) \
    cpi_inflation_yoy_pct(-2) cpi_inflation_yoy_pct(-12) \
    oil_volatility_3m(-1) usd_inr_change_pct --robust
```

The robust option reports HAC/Newey–West standard errors using a Bartlett kernel and bandwidth 4. These standard errors adjust inference for heteroskedasticity and autocorrelation in the estimated covariance matrix; they do not correct an incorrectly specified conditional-mean model.

### Model estimates

| Variable                          | Coefficient | Conventional OLS SE | Conventional OLS p-value |   HAC SE | HAC p-value |
| --------------------------------- | ----------: | ------------------: | -----------------------: | -------: | ----------: |
| Constant                          |    0.880365 |            0.288063 |                   0.0027 |       — |      0.0050 |
| CPI inflation, lag 1              |    1.086290 |            0.085648 |                   <0.001 | 0.086113 |      <0.001 |
| CPI inflation, lag 2              |  −0.220535 |            0.089756 |                   0.0154 | 0.085845 |      0.0114 |
| CPI inflation, lag 12             |  −0.072007 |            0.042144 |                   0.0900 | 0.037902 |      0.0597 |
| Three-month oil volatility, lag 1 |    0.015053 |            0.008836 |                   0.0909 | 0.005223 |      0.0046 |
| INR/USD percentage change         |  −0.017672 |            0.054621 |                   0.7468 | 0.060050 |      0.7690 |

The constant's HAC p-value is included as reported by Gretl; its HAC standard error was not available in the summarized output used to prepare this log.

**Model fit:** \(R^2=0.814433\); adjusted \(R^2=0.807069\); residual standard error \(=0.700795\); AIC \(=286.5968\); BIC \(=303.8936\); HQC \(=293.6254\).

### Interpretation

1. The coefficient on one-month-lagged three-month oil volatility is positive (\(0.015053\)) and statistically significant at the 5% level using HAC inference (\(p=0.0046\)).
2. Conditional on the included inflation lags and exchange-rate change, higher oil volatility in the previous month is associated with higher current CPI inflation in this specification.
3. The contemporaneous oil-volatility measure in Model 5 was not statistically significant. The timing in Model 6 therefore matters to the empirical result.
4. Inflation is persistent: the first and second monthly lags are statistically significant under HAC inference. The 12-month lag is marginal and is not significant at 5% (\(p=0.0597\)).
5. The monthly INR/USD percentage change is not statistically significant in Model 6 (\(p=0.7690\)).
6. The estimated relationship is conditional and observational. It does not establish that oil volatility causes inflation, and it should not be described as a definitive causal effect.

The oil-volatility coefficient is in percentage-point units of the constructed volatility measure, not a direct elasticity. Interpret its magnitude with the exact construction of `oil_volatility_3m` in mind.

## 14. Final diagnostics and inference limitations

### Heteroskedasticity

The White test for Model 6 returned \(p=0.318692\). At conventional significance levels, the null of homoskedasticity is not rejected. This is not proof that the error variance is constant; HAC inference is retained as a conservative approach to inference under possible heteroskedasticity and serial dependence.

### Residual autocorrelation

The Model 6 Breusch–Godfrey tests through order 12 reject the null of no residual autocorrelation:

| Test                  | Statistic |               p-value |
| --------------------- | --------: | --------------------: |
| Breusch–Godfrey LMF  |  4.125749 |  \(2.4\times10^{-5}\) |
| Breusch–Godfrey TR² |  39.96836 | \(7.28\times10^{-5}\) |
| Ljung–Box\(Q'\)      |   50.5686 | \(1.11\times10^{-6}\) |

Residual autocorrelation remains a material limitation. HAC standard errors can make coefficient inference more robust to serial correlation, but they do not eliminate the residual pattern or establish that the dynamic specification is complete. The results should therefore be presented as evidence under the selected specification, not as the last word on the inflation process.

### Stationarity and structural breaks

The earlier ADF checks showed specification and lag sensitivity for CPI inflation and the oil-price level. Oil log returns and INR/USD percentage changes rejected the unit-root null under the reported six-lag specifications. COVID-19, the 2014–2016 oil-price decline and the 2022 energy shock may affect standard unit-root tests. The ordinary ADF test on Model 2 residuals is not a formal cointegration test using residual-based critical values; it should not be used to claim cointegration.

### Scope of the analysis

- The analysis is monthly and uses a relatively small sample.
- The model does not include every potential driver of Indian inflation, such as food prices, domestic fuel policy, monetary policy, output conditions or global supply disruptions.
- A three-month rolling standard deviation is one operational measure of oil-price volatility; other volatility measures may produce different estimates.
- Statistical significance is conditional on the variables, sample, lag structure and inference method used.
- No causal identification strategy has been implemented.

## 15. Data sources and data handling notes

Use the following source pages in the final report and retain the downloaded source files alongside the cleaned dataset.

1. **Crude oil:** Petroleum Planning & Analysis Cell (PPAC), international crude oil prices / Indian Basket historical data:https://ppac.gov.in/index.php/prices/international-prices-of-crude-oil
2. **CPI:** RBI Database on Indian Economy (DBIE), Consumer Price Index table:https://dev.dbie.rbihub.in/prices?table=real_sector.r45_consumer_price_index
3. **Exchange rate:** RBI DBIE, “Average forex rate” table:
   https://dev.dbie.rbihub.in/statistics?table=financial_markets.avg_for_rat_rn

For the exchange-rate series, select the **UNITED STATES DOLLAR** column, with the unit in Indian rupees and monthly frequency. This is the monthly average INR per USD series; it is not the RBI's purchase/sale transaction-rate data. A positive change in INR per USD means rupee depreciation.

The CPI series uses the Combined CPI, Base 2012=100. The year-on-year inflation series should be cross-checked against the index using the year-on-year percentage-change formula, allowing for rounding. Keep the December 2025 observation in the sample based on the source validation noted above; do not delete observations merely because they are unusually large or small.

## 16. Overall conclusion

The initial contemporaneous regressions did not find statistically significant relationships between monthly oil-price changes and CPI inflation. Once inflation persistence was modelled, the fit improved substantially, but residual autocorrelation remained. In the final dynamic specification, one-month-lagged three-month oil volatility had a positive coefficient and was statistically significant using HAC standard errors (\(0.015053\), \(p=0.0046\)). The exchange-rate change was not significant.

The most defensible conclusion is therefore:

> The analysis finds evidence of a positive conditional association between lagged crude-oil price volatility and Indian CPI inflation in the selected dynamic specification. This result is not evidence of causation, and residual autocorrelation, lag sensitivity, possible structural breaks and omitted variables limit the strength of the conclusion.

This completes the current exploratory research log. Further work should be driven by the course requirements or a clearly motivated research question, rather than adding tests solely to chase a more favourable result.
