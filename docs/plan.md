# Overview
This project analyses world population estimates and projections. 


# Questions
- Are population increases due more to immigration or natural increase?
    - Probably differs by country, but likely due to natural increase.
    - YR, GEO_ID, GR, POP, BIRTHS, DEATHS, NATINCR (natural increase: births - deaths), NIM, NMR, RNI
<p></p>

- How does Covid / Recession affect population, birth rates, life expectancy?
    - Steady / lower population, lower birth dates, lower life expectancy.
    - YR, GEO_ID, GR, POP, BIRTHS, DEATHS, NATINCR (natural increase: births - deaths), E0, E0_F, E0_M
<p></p>

- How has the age at which women have children changed over time?
    - Increase age that women have children - because of increase life expectancy & general knowledge (less stay at home moms, entering the workforce, more birth control options)
    - All BIRTHS* columns, YR, GEO_ID


# Explore
- Visualize with slider population pyramid (single year dataset)


# Process
Project process is as follows (subject to change)

## Plan
| Task | Est. Time | Act. Time |
| ---- | --------- | --------- |
| Explore datasets | 1 hr | 45 min |
| Create hypothesis questions | 15 min | 10 min |
| Create project plan | 1 hr | 45 min |
| Total | ~2:15 hrs | 1:40 hrs |

## Prep
| Task | Est. Time | Act. Time |
| ---- | --------- | --------- |
| Create new GitHub repo | 5 min | 3 min |
| Set up folders and .venv | 5 min | 10 min |
| Create entity relationship diagram | 45 min | 1 hr |
| Total | ~0:55 min | 1:13 hrs |

## Transform
| Task | Est. Time | Act. Time |
| ---- | --------- | --------- |
| Create schema with DDL | 1 hr | 40 min |
| Load in raw data | 10 min | 30 min |
| Filter down for only the I need | 2 hr | 3:50 hrs |
| Total | ~2:30 hrs | 5 hr |

## Load
| Task | Est. Time | Act. Time |
| ---- | --------- | --------- |
| Load transformed data into DB | 1 hr | 2:25 hrs |
| Total | ~1 hr | 2:25 hrs |

## App
| Task | Est. Time | Act. Time |
| ---- | --------- | --------- |
| Sketch up possible app view | 15 min | 45 min |
| Load data tables in | 1 hr | 3:10 hrs |
| Create population section | 2 hr | 2 hr |
| Create recession section | 2 hr | 3:15 hrs |
| Create birth changes section | 3 hr | 1:15 hrs |
| App final touches | 2 hr | 2:15 hrs |
| Total | ~10:15 hrs | 12:40 hrs |

## Report
| Task | Est. Time | Act. Time |
| ---- | --------- | --------- |
| Overview section | 30 min | 1:15 hrs |
| Questions / hypothesis section | 15 min | 10 min |
| Data description section | 30 min | 15 min |
| EDA / Analysis section | 2 hr | 55 min |
| App section | 1 hr | 15 min |
| ETL / Code / Technical section | 1 hr | 35 min |
| Sources section | 15 min | 10 min |
| Total | ~5:30 hrs | 3:35 hrs |