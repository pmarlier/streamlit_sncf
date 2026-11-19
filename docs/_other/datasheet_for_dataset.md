# Dataset Datasheet

> Working template inspired by Gebru et al., “Datasheets for Datasets” (2021). It is intended to document the project’s datasets.
>

## 1. Identification and Motivation

- **Dataset name:** regularite-mensuelle-tgv-aqst.csv
- **Version or reference date:** October 17th, 2026
- **Datasheet owner:** SNCF Voyageurs
- **Date created / last updated:** October 2nd, 2026 / October 17th, 2026
- **Why was this dataset created or selected?** SNCF Streamlit project
- **What task or need is it intended to address?** Give customer an overview of traffic state on a trip (e.g. for planning) : train reliability, based on train delays, cancellations (amount, time and causes) for a given period of time.
- **Who created it, and on behalf of which organization?** SNCF Voyageurs
- **Who funded its creation, if applicable?** N/A
- **Other comments:**N/A

## 2. Composition

- **What does one row (or instance) represent?** The TGV connexion (departure to arrival station trip) for a given month, trakced by SNCF.
- **What types of instances does it contain?** integers, strings, floats
- **How many instances does it contain?** 12544 instances × 26 features
- **What is its temporal and geographic coverage?** Geographic coverage maps whole France TGV stations, and neighbor connecting countries (Barcelona, Madrid, Zurich, Francfort, Stuttgart, Genova, Lausanne, Italy).
- **Is it a sample?** No, it is the set of TGV routes monitored by the SNCF.
- **What variables does it contain?** 
  - 4 identification columns: date, service (National: 11,012 rows; International: 1,532 rows), departure and arrival stations;
  - average trip duration;
  - planned circulations and cancelled trains;
  - delays at departure and at arrival: counts and means, with or without on-time trains;
  - trains delayed by more than 15, 30 and 60 minutes;
  - 6 columns of delay-cause percentages;
  - 3 comment columns.
- **Are there targets, labels, or relationships between instances?** none, the dataset is descriptive.
- **Are any missing values, errors, duplicates, or sources of noise known?** 
  - 0 missing values in the numeric columns;
  - the cancellation and departure comment columns are 100 % empty; the arrival comment column is filled in only 698 rows;
  - 84 rows are duplicated on (date, departure, arrival), i.e. 42 routes present in both National and International services, which the project merges;
  - 73 rows have 0 planned circulations;
  - 63 rows have more cancelled trains than planned circulations;
  - 31 rows have more trains delayed by more than 15 min than trains delayed at arrival;
  - 40 rows have delayed trains but a mean delay ≤ 0;
  - negative mean delays exist, down to −472 min (53 values below −1 min at arrival);
  - delay causes that do not sum to 100 %: 275 rows below 99.9 %, 270 of them at 0.
- **Does the dataset depend on other files, datasets, or external services?** `liste-des-gares.csv` (6,469 rows) and `lignes-par-region-administrative.csv` (2,909 rows) for the map. They are joined through a hand-written name mapping in `railway_data/__init__.py`.
- **Are recommended splits available** (training, validation, test)? N/A
- **Does the dataset relate to people or allow them to be identified directly or indirectly?** N/A
- **Does it contain confidential or sensitive information, or information that could cause harm?** N/A
- **Other comments:** N/A

## 3. Collection Process

- **How was the data obtained?** Via third-party SNCF Voyageurs, via open data, aggregated monthly
- **What procedures, sources, tools, or APIs were used?** The raw csv file has been downloaded once, and stored in data/raw.
- **What sampling strategy was used, if applicable?** N/A
- **When was the data collected?** It was collected in September 2026, including data up to 06/2026.
- **Who was involved in data collection, and under what conditions?** Only project contributors
- **If people are involved:** N/A
- **Was an ethics review or impact assessment conducted?** N/A
- **Other comments:** N/A

## 4. Preprocessing, Cleaning, and Labeling <span style="color:orange">[TBD @Christophe]</span>

- **What transformations were applied?** Describe cleaning, filtering, conversions, imputation, and labeling. 
  - Data from the COVID-19 disruption period (March 2020 to June 2021) are invalidated (`NaN`) as they are not representative of normal railway operations.
  - Delay indicators greater than 30 and 60 minutes are invalidated for Q1 2025 due to data quality issues.
  - Inconsistent delay values are corrected or invalidated (`NaN`).
  - Missing or invalid average arrival delays are imputed using historical medians for the same service, route, and month when sufficient historical data exist.
  - A new feature, **"Prct retard causes non renseignées"**, is computed so that all delay-cause percentages sum to 100%.
  - No records are removed; unreliable values are either corrected, imputed, or marked as missing.

- **Is the raw data retained?** Where can it be accessed? <span style="color:orange">[To be completed]</span>
- **What tools, scripts, and versions were used?** <span style="color:orange">[To be completed]</span>
- **Other comments:** <span style="color:orange">[To be completed]</span>

## 5. Uses

- **What has the dataset already been used for?** For a dataset overview, summarizing statistics on the full dataset, inconditionnaly of connections and periods.
https://public.tableau.com/app/profile/aur.lien8073/viz/snc_15838585145650/TGV
- **What other uses are envisioned?** N/A
- **What uses are discouraged or unsuitable, and why?** 
  - comparing routes over different periods without accounting for COVID;
  - interpreting the >30 and >60 min delays of Q1 2025 (invalidated);
  - drawing conclusions about an individual train: only monthly averages are available.
- **What limitations in coverage, quality, or collection could affect results?** 
  - The covid years of 2019 and 2020 appears to be exceptionnal in terms of trends in delays and cancellations. Regarding the features, those considerations must be addressed.
  - Averages of averages are biased if they are not weighted by the number of trains.
- **References to work or systems that use the dataset:** N/A

## 6. Distribution and Access

- **Is the dataset shared outside the organization?** Public dataset
- **Where and how can it be accessed?** 
  - [GitHub repository](https://github.com/pmarlier/streamlit_sncf/tree/main)
  - <span style="color:orange">Application website</span>
- **Release date and persistent identifier (DOI), if applicable:** 20/11/2026
- **What license or terms of use apply?** N/A
- **Do any third-party rights or restrictions apply?** N/A
- **Are any fees, export controls, or other regulatory restrictions reported?** N/A
- **Other comments:** N/A

## 7. Maintenance

- **Who hosts, maintains, and updates the dataset?** Pierre Marlier, Ulysse Perruchon-Monge, Christophe Vandenborre - Télécom Paris
- **How can the owner be contacted?** [Via github repository](https://github.com/pmarlier/streamlit_sncf/tree/main)
- **Is there an erratum or a channel for reporting issues?** [Via github repository](https://github.com/pmarlier/streamlit_sncf/tree/main)
- **How are older versions retained and identified?** N/A
- **Are there data retention or deletion rules?** N/A
- **Can external contributions or corrections be submitted?** N/A
- **Other comments:** N/A

## 8. Project Source Inventory

Add one row per file or source. Duplicate the sections above if a source needs its own datasheet.

| File or source | Description | Period / coverage | Provenance and access | License / restrictions |
| --- | --- | --- | --- | --- |
| `data/raw/regularite-mensuelle-tgv-aqst.csv` | SNCF TGVs monthly regularity per connexion | 01/2018 to 06/2026 | ressources.data.sncf.com | Open Database License (ODbL) |


## Reference

Gebru, Timnit, et al. “Datasheets for Datasets.” *Communications of the ACM*, 2021. [arXiv:1803.09010](https://arxiv.org/abs/1803.09010).