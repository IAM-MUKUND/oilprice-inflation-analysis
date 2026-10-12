# Does Crude Oil Price Volatility Affect Inflation in India?

## Econometric Analysis --- Research Log

**Status:** Exploratory analysis in progress\
**Software:** Gretl 2026c-git\
**Frequency:** Monthly\
**Merged data:** January 2013--December 2025\
**Current regression sample:** January 2014--December 2025

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

  -----------------------------------------------------------------------
  Variable                            Meaning
  ----------------------------------- -----------------------------------
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
  -----------------------------------------------------------------------

Definitions: - Oil percentage change =
`100 × (P_t − P_(t−1)) / P_(t−1)` - Oil log return =
`100 × (ln(P_t) − ln(P_(t−1)))` - Three-month volatility = rolling
sample standard deviation of the current and previous two oil log
returns. - INR/USD percentage change =
`100 × (FX_t − FX_(t−1)) / FX_(t−1)`. A positive value indicates rupee
depreciation.

## 3. Descriptive statistics

For the 144-observation sample:

  -------------------------------------------------------------------------------
  Variable               Mean       Median      Minimum      Maximum         Std.
                                                                        deviation
  -------------- ------------ ------------ ------------ ------------ ------------
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
  -------------------------------------------------------------------------------

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

-   Oil prices fell sharply in 2015--2016 and around 2020, then
    recovered and rose around 2022.
-   CPI inflation varies over the sample, with a pronounced decline at
    the end of 2025 that requires source verification.
-   INR per USD generally trends upward, consistent with long-run rupee
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
  ---------------------- --------------- ---------
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

``` gretl
ols cpi_inflation_yoy_pct const oil_change_pct usd_inr_change_pct
series baseline_residuals = $uhat
series baseline_fitted = $yhat
modtest 12 --autocorr
```

Sample: January 2014--December 2025, T = 144.

  Variable             Coefficient   Std. error   p-value
  ------------------ ------------- ------------ ---------
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
  ---------------------- ----------- --------------
  Breusch--Godfrey LMF       43.3864   2.04 × 10⁻³⁹
  Breusch--Godfrey TR²      115.4056   5.07 × 10⁻¹⁹
  Ljung--Box Q′               344.04   2.54 × 10⁻⁶⁶

All tests reject the null of no residual autocorrelation through order
12. Conventional OLS inference is questionable under this residual
pattern.

## 7. Model 2 --- add inflation persistence

Gretl command:

``` gretl
ols cpi_inflation_yoy_pct const cpi_inflation_yoy_pct(-1) oil_change_pct usd_inr_change_pct
series model2_residuals = $uhat
series model2_fitted = $yhat
modtest 12 --autocorr
```

Sample: February 2014--December 2025, T = 143.

  Variable                           Coefficient   Std. error        p-value
  -------------------------------- ------------- ------------ --------------
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
  ---------------------- ----------- -------------
  Breusch--Godfrey LMF        5.5290   1.54 × 10⁻⁷
  Breusch--Godfrey TR²       49.0708   2.03 × 10⁻⁶
  Ljung--Box Q′              67.1685   1.08 × 10⁻⁹

All tests reject the null of no residual autocorrelation through order
12. Diagnostics improved relative to Model 1, but significant
autocorrelation remains. The high R² does not by itself establish model
adequacy.

## 8. Step 9 --- ADF test on Model 2 residuals

Gretl command:

``` gretl
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

1.  Inflation is strongly persistent in Model 2.
2.  Contemporaneous monthly oil-price changes are statistically
    insignificant in Models 1 and 2.
3.  Contemporaneous INR/USD changes are statistically insignificant in
    Models 1 and 2.
4.  Model 2 fits the sample far better than Model 1, but significant
    residual autocorrelation remains.
5.  ADF evidence for CPI inflation and the oil-price level is sensitive
    to specification and lag order.
6.  No causal conclusion has been established.

These are preliminary findings, not the final answer to the research
question.

## 10. Next steps

The immediate next stage should be a focused dynamic-specification check
rather than more arbitrary ADF lag testing:

1.  Verify the source values and metadata for the sharp CPI decline at
    the end of 2025.
2.  Inspect Model 2 residual ACF/PACF to understand the remaining serial
    pattern.
3.  Test a small number of theoretically motivated specifications, such
    as lagged oil-price changes or the pre-defined oil-volatility
    measure. Keep the model parsimonious.
4.  Re-run residual diagnostics after each meaningful specification
    change. Do not select a model solely because it raises R² or gives a
    preferred p-value.
5.  Consider HAC/Newey--West standard errors for inference after
    clarifying the model. These can help account for heteroskedasticity
    and autocorrelation in standard errors, but do not repair a
    misspecified dynamic model.
6.  Revisit stationarity and structural breaks for the final
    specification. Do not infer cointegration from the ordinary residual
    ADF p-value above.

**Immediate next action:** inspect Model 2 residual ACF/PACF and verify
the end-2025 CPI observations before choosing one small alternative
specification.

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
