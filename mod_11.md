```mermaid
flowchart LR


tp_winter -->|1| lai_spring
t2m_winter -->|2| lai_spring

tp_winter -->|3| sm_summer
t2m_winter -->|4| sm_summer

tp_winter -->|5| sd_spring
t2m_winter -->|6| sd_spring

lai_spring -->|7| lai_summer
sm_summer -->|8| lai_summer

sd_spring --> |9| lai_summer

tp_winter -->|10| lai_summer
t2m_winter -->|11| lai_summer

```