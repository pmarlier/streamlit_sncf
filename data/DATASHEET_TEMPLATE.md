# Dataset Datasheet

> Working template inspired by Gebru et al., “Datasheets for Datasets” (2021). It is intended to document the project’s datasets; it is not a legal or ethical certification.
>
> **Instructions:** Make a copy of this datasheet when sources have different characteristics. Answer using the information available; write “Unknown,” “To be confirmed,” or “Not applicable” rather than leaving ambiguity. Do not include personal or confidential data in this document.

## 1. Identification and Motivation

- **Dataset name:** regularite-mensuelle-tgv-aqst.csv
- **Version or reference date:** October 17th, 2026
- **Datasheet owner:** SNCF
- **Date created / last updated:** October 2nd, 2026 / October 17th, 2026
- **Why was this dataset created or selected?** SNCF Streamlit project
- **What task or need is it intended to address?** Give customer an overview of traffic state on a trip (e.g. for planning) : train reliability, based on train delays, cancellations (amount, time and causes) for a given period of time.
- **Who created it, and on behalf of which organization?** SNCF Voyageurs
- **Who funded its creation, if applicable?** <span style="color:orange">[To be completed]</span>
- **Other comments:** <span style="color:orange">[To be completed]</span>

## 2. Composition

- **What does one row (or instance) represent?** A month of a given year
- **What types of instances does it contain?** integers, strings, floats
- **How many instances does it contain?** <span style="color:red">12544 instances over 10 features</span> # tobe confirmed
- **What is its temporal and geographic coverage?** Geographic coverage maps whole France TGV stations, and neighbor connecting countries (spain, germany, switzerland, italy and Bretagne)
- **Is it a sample?** Describe the source population, selection method, and any limitations on representativeness. <span style="color:orange">[To be completed]</span>
- **What variables does it contain?** Describe their meaning, type, units, and possible values. <span style="color:orange">[To be completed]</span>
- **Are there targets, labels, or relationships between instances?** <span style="color:orange">[To be completed]</span>
- **Are any missing values, errors, duplicates, or sources of noise known?** <span style="color:orange">[To be completed]</span>
- **Does the dataset depend on other files, datasets, or external services?** Describe the dependencies and any restrictions. <span style="color:orange">[To be completed]</span>
- **Are recommended splits available** (training, validation, test)? <span style="color:orange">[To be completed]</span>
- **Does the dataset relate to people or allow them to be identified directly or indirectly?** <span style="color:orange">[To be completed]</span>
- **Does it contain confidential or sensitive information, or information that could cause harm?** Describe any relevant safeguards. <span style="color:orange">[To be completed]</span>
- **Other comments:** <span style="color:orange">[To be completed]</span>

## 3. Collection Process

- **How was the data obtained?** Specify whether it was observed, reported, provided by a third party, or inferred. <span style="color:orange">[To be completed]</span>
- **What procedures, sources, tools, or APIs were used?** How were they validated? <span style="color:orange">[To be completed]</span>
- **What sampling strategy was used, if applicable?** <span style="color:orange">[To be completed]</span>
- **When was the data collected?** Does this differ from the time period represented by the data? <span style="color:orange">[To be completed]</span>
- **Who was involved in data collection, and under what conditions?** <span style="color:orange">[To be completed]</span>
- **If people are involved:** Were they notified, and was their consent obtained? Describe the process and any means of withdrawal, if applicable. <span style="color:orange">[To be completed]</span>
- **Was an ethics review or impact assessment conducted?** Indicate where supporting documentation can be found. <span style="color:orange">[To be completed]</span>
- **Other comments:** <span style="color:orange">[To be completed]</span>

## 4. Preprocessing, Cleaning, and Labeling

- **What transformations were applied?** Describe cleaning, filtering, conversions, imputation, and labeling. <span style="color:orange">[To be completed]</span>

<span style="color:green">
Christophe
</span>

<span style="color:yellow">
Pierre
</span>

<span style="color:red">
Ulysse
- For delayed/cancelled trains for a given connection, months time period and years, the years 2019 anbd 2020 will'nt be considered because not reprensentative of a standard flow (covid years).
</span>

- **Is the raw data retained?** Where can it be accessed? <span style="color:orange">[To be completed]</span>
- **What tools, scripts, and versions were used?** <span style="color:orange">[To be completed]</span>
- **Other comments:** <span style="color:orange">[To be completed]</span>

## 5. Uses

- **What has the dataset already been used for?** For a dataset overview, summarizing statistics on the full dataset, inconditionnaly of connections and periods.
https://public.tableau.com/app/profile/aur.lien8073/viz/snc_15838585145650/TGV
- **What other uses are envisioned?** <span style="color:orange">[To be completed]</span>
- **What uses are discouraged or unsuitable, and why?** <span style="color:orange">[To be completed]</span>
- **What limitations in coverage, quality, or collection could affect results?** The covid years of 2019 and 2020 appears to be exceptionnal in terms of trends in delays and cancellations. Regarding the features, those considerations must be addressed.
- **References to work or systems that use the dataset:** <span style="color:orange">[To be completed]</span>

## 6. Distribution and Access

- **Is the dataset shared outside the organization?** With whom, and under what conditions? No
- **Where and how can it be accessed?** Provide a URL, repository, API, or internal path, as applicable. <span style="color:red">To be provided after deployment</span>
- **Release date and persistent identifier (DOI), if applicable:** <span style="color:orange">[To be completed]</span>
- **What license or terms of use apply?** Provide a link to the applicable terms. <span style="color:orange">[To be completed]</span>
- **Do any third-party rights or restrictions apply?** <span style="color:orange">[To be completed]</span>
- **Are any fees, export controls, or other regulatory restrictions reported?** <span style="color:orange">[To be completed]</span>
- **Other comments:** <span style="color:orange">[To be completed]</span>

## 7. Maintenance

- **Who hosts, maintains, and updates the dataset?** <span style="color:orange">Pierre Marlier, Ulysse Perruchon-Monge, Christophe Vandenborre - Télécom Paris</span>
- **How can the owner be contacted?** <span style="color:orange">[To be completed]</span>
- **Is there an erratum or a channel for reporting issues?** <span style="color:orange">[To be completed]</span>
- **Will the dataset be updated?** Monthly
- **How are older versions retained and identified?** <span style="color:orange">[To be completed]</span>
- **Are there data retention or deletion rules?** <span style="color:orange">[To be completed]</span>
- **Can external contributions or corrections be submitted?** Describe how they are validated and distributed. <span style="color:orange">[To be completed]</span>
- **Other comments:** <span style="color:orange">[To be completed]</span>

## 8. Project Source Inventory

Add one row per file or source. Duplicate the sections above if a source needs its own datasheet.

| File or source | Description | Period / coverage | Provenance and access | License / restrictions |
| --- | --- | --- | --- | --- |
| `data/raw/regularite-mensuelle-tgv-aqst.csv` | SNCF TGVs monthly regularity per connexion | 01/2018 to current month | ressources.data.sncf.com | Open Database License (ODbL) |


## Reference

Gebru, Timnit, et al. “Datasheets for Datasets.” *Communications of the ACM*, 2021. [arXiv:1803.09010](https://arxiv.org/abs/1803.09010).