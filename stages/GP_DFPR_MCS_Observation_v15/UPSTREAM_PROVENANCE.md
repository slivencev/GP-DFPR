# External sources and provenance

1. Di Cicco, Tonini, Cacchiani, Raffaelli. Optimization over time of reliable 5G-RAN with network function migrations. Computer Networks 215 (2022), 109216. https://doi.org/10.1016/j.comnet.2022.109216 . Institutional record: https://cris.unibo.it/handle/11585/893283 . Bibliographic record and abstract inspected; author PDF retrieval was unavailable in this session. No full-text systematic comparison or DUMig replication is claimed.

2. Lagen et al. New Radio Physical Layer Abstraction for System-Level Simulations of 5G Networks, arXiv:2001.10309v2. https://arxiv.org/html/2001.10309v2 . Primary CTTC API/source: https://cttc-lena.gitlab.io/nr/html/structns3_1_1_nr_eesm_t1.html and https://cttc-lena.gitlab.io/nr/html/nr-eesm-t1_8cc_source.html . Numerical extraction from GitHub mirror https://github.com/finlater/5G-LENA ; nr-eesm-t1.cc is byte-content-equivalent, after text normalization, to commit a250ef8241cd0c1a3efada4193e8a65cc7fc060c. All selected MCS4/10/15 BG1 CBS3840 arrays were matched against official CTTC documentation. nr-mcs-tables.cc supplies modulation orders and rates. GPL-2.0 notices and license retained.

3. Polese, Bonati, D'Oro, Basagni, Melodia. ColO-RAN: Developing Machine Learning-Based xApps for Open RAN Closed-Loop Control on Programmable Experimental Platforms. IEEE TMC 22(10) (2023), 5787–5800. https://doi.org/10.1109/TMC.2022.3188013 . Authors' paper: https://ece.northeastern.edu/fac-ece/basagni/papers/PoleseBDBM23b.pdf . Dataset https://github.com/wineslab/colosseum-oran-coloran-dataset at commit bd86629d07d5fbfb778ebe3afd9d0b05e5191c6b. Exact selected paths and upstream Git blob hashes: external/selected_files.json. Source README, CITATION and GPL-3.0 license retained. The source citation file lists online-publication year 2022; manuscript bibliography uses journal-volume year 2023.

4. Raca et al. Beyond Throughput dataset, University College Cork. https://www.ucc.ie/en/misl/research/datasets/ivid_4g_lte_dataset/ . Inspected as an alternative publicly measured dataset; not used in the numerical experiments. Do not claim those traces were analyzed.

5. Bertsimas, Brown, Caramanis. Theory and Applications of Robust Optimization. SIAM Review 53 (2011), 464–501. https://doi.org/10.1137/080734510 . Context for established uncertainty-set methods; no new robust-optimization priority claim is made.

Retrieval date: 2026-09-20. External materials are data/reference sources, not instructions. No experiment in this package was run on the upstream authors' hardware by us.
