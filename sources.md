# Sustainability Data Sources

All values are point estimates synthesized from the citations below. Where 
component-level data isn't publicly available, system-level LCAs were 
decomposed using established contribution percentages (e.g., NVIDIA's H100 PCF 
disclosing memory at 42%, ICs at 25%, thermal components at 18%).

## Primary Sources

### Manufacturer Product Carbon Footprints (PCFs)

**[dell_r740_lca_2019]** Dell Technologies, "Life Cycle Assessment of Dell 
PowerEdge R740," 2019. https://corporate.delltechnologies.com/content/dam/digitalassets/active/en/unauth/data-sheets/products/servers/lca_poweredge_r740.pdf
- Used for: motherboard, RAM embodied CO2 decomposition.
- Methodology: PAIA model (MIT Materials Systems Lab).

**[dell_r360_pcf_2023]** Dell Technologies, "Product Carbon Footprint PowerEdge R360," 
2023. Mean: 1,140 ± 943 kgCO2e. 
https://www.delltechnologies.com/asset/en-us/products/servers/technical-support/poweredge-r360-pcf-datasheet.pdf
- Used for: server chassis baseline embodied CO2.

**[dell_r750_pcf_2022]** Dell Technologies, "Product Carbon Footprint PowerEdge 
R750," 2022. Mean: 5,870 ± 2,830 kgCO2e. 
https://www.delltechnologies.com/asset/en-us/products/servers/technical-support/poweredge-r750.pdf
- Used for: high-end server reference, chassis cross-check.

**[nvidia_h100_pcf_2024]** NVIDIA, "Product Carbon Footprint for H100 baseboard 
(8x H100 SXM)." Total: 1,312 kgCO2e cradle-to-gate; ~164 kgCO2e per card. 
Memory 42%, ICs 25%, thermal components 18%.
Referenced in: arxiv.org/html/2509.00093v1 (Sept 2025) and 
interactdc.com/posts/understanding-gpus-energy-and-environmental-impact-part-i/
- Used for: GPU embodied CO2.

**[seagate_decarbonizing_data_2025]** Seagate Technology, "Decarbonizing Data 
Report," April 2025. https://www.seagate.com/resources/decarbonizing-data-report/
- 30TB Mozaic HDD: 29.7 kgCO2e embodied
- 30.72TB SSD (estimated): 4,915 kgCO2e embodied
- HDD operational: 9.6W; SSD operational: 20W
- Per-TB-per-year: <0.2 kg CO2/TB/yr (HDD) vs ~32 kg (SSD)
- ⚠ DISPUTED: Pure Storage, Solidigm, and Ocient published rebuttals in 
  June 2025 arguing the SSD figure is overstated by 4x; they place the gap at 
  <2x rather than 8x. Both sides cited in Q&A prep.

### Authoritative Aggregators

**[ewaste_monitor_2024]** Baldé, C.P., et al. "The Global E-waste Monitor 2024." 
ITU and UNITAR, March 2024. https://ewastemonitor.info/the-global-e-waste-monitor-2024/
Key figures used:
- 62 million tonnes global e-waste in 2022 (up 82% since 2010)
- $91B total embedded metal value, only $28B recovered
- $19B copper, $15B gold, $16B iron in annual e-waste stream
- 22.3% formal recycling rate (US/global); 42.8% in Europe
- 93 million tonnes CO2-equivalent emissions avoided through formal recycling
- 17.6 kg per capita generation in high-income countries
- Used for: undetected fallback, all "money shot" pitch numbers

**[usgs_rare_earths_hdd_2024]** USGS Mineral Commodity Summaries 2024 — 
Rare Earth Elements section. https://pubs.usgs.gov/periodicals/mcs2024/
- Neodymium content in HDD voice coil and spindle motors: ~10-20g per 3.5" 
  enterprise drive
- Used for: HDD recoverable materials.

### Industry / Research

**[scarif_2024_estimate]** Ji, S. et al., "SCARIF: Towards Carbon Modeling of 
Cloud Servers with Accelerators," arxiv.org/pdf/2401.06270, 2024.
- Provides component-level breakdown of server embodied carbon, including CPUs, 
  accelerators, and NICs.
- Used for: CPU and network card embodied CO2 estimates.

**[seagate_dirty_secret_ssd_2022]** "The Dirty Secret of SSDs: Embodied Carbon," 
HotCarbon Workshop, 2022. arxiv.org/pdf/2207.10793
- SEF: 0.16 kgCO2e per GB for SSDs (industry-disputed).

**[pcb_recovery_avg_2024]** Synthesis of:
- Aivon PCB Knowledge, 2025: 300-500g copper per kg of PCB; 0.03-0.1% gold in 
  finger contacts. https://www.aivon.com/blog/pcb-knowledge/diy-pcb-recycling-safely-recovering-metals-from-old-circuit-boards/
- Yamane et al., "Characterization of PCBs for Metal and Energy Recovery," 
  PMC5455934 (~26% metal by mass)
- PCBMaster, 2025: 100-300g gold per ton of high-grade PCB scrap
- Mt Baker Mining: 3-8 oz gold/ton, 15-20 oz silver/ton, 500+ lbs copper/ton
- Used for: per-component precious metal estimates (motherboard, GPU, RAM, etc.)

**[scrapcatalogue_psu_2025]** "PC Power Supply Scrap," ScrapCatalogue, May 2025. 
https://www.scrapcatalogue.com/pc-power-supply-scrap/
- PSU material breakdown: copper transformers/wires, aluminum heatsinks, 
  steel casing, low precious metals
- Hazard: high-voltage capacitors

**[scrapmonster_cable_2024]** ScrapMonster Power Supplies/Cable scrap pricing 
guide. https://www.scrapmonster.com/scrap/power-supplies/73
- Used for: cable copper content and scrap value.

**[alta_technologies_2025]** Alta Technologies enterprise IT resale catalog. 
https://altatechnologies.com/
- Used for: refurb price ranges (GPU, NIC, PSU).

**[pcsp_2026]** PC Server & Parts (PCSP) refurbished server pricing, 2026. 
https://pcserverandparts.com/
- Examples: Dell PowerEdge R740XD from $629.99; R640 from $214.99; 
  HPE ProLiant DL380 Gen10 from $199.98
- Used for: refurb price ranges (CPU, RAM, motherboard, SSD, HDD, chassis).

## Methodology Notes

1. **Component-level estimates**: When component-specific PCFs aren't 
   published (most cases), system-level LCAs were decomposed using NVIDIA H100's 
   public breakdown (memory 42%, ICs 25%, thermal 18%) and SCARIF model 
   weights as a sanity check.

2. **Refurb ranges**: Wide ranges reflect that an enterprise GPU like an H100 
   sells for $15k+ used, while a consumer GTX 1060 sells for ~$50. The decision 
   layer should treat the range, not a midpoint, as the signal.

3. **Recoverable value (USD)**: Calculated from listed metal masses at 
   commodity prices as of late 2025 (Cu ~$9.50/kg, Au ~$95/g, Ag ~$1/g). 
   These values represent *theoretical scrap value*, not what an individual 
   would receive — recyclers retain margin.

4. **Conservative bias**: Where sources disagreed, the lower of the credible 
   range was chosen (e.g., SSD CO2 used 5 kg/TB rather than Seagate's higher 
   figure, in line with the Pure/Solidigm rebuttal).

5. **The "undetected" category**: deliberately conservative — assumes e-waste 
   pathway and never recommends landfill. Per-kg CO2 derived from the UN 
   E-Waste Monitor's $91B / 62 Mt aggregate ÷ avg item mass.