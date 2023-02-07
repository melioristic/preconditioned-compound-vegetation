```mermaid
flowchart LR


tp_winter -->|1| lai_spring
t2m_winter -->|2| lai_spring

tp_winter -->|3| sm_summer
t2m_winter -->|4| sm_summer

lai_spring -->|5| lai_summer

sm_summer -->|6| lai_summer

tp_winter -->|7| lai_summer
t2m_winter -->|8| lai_summer

```