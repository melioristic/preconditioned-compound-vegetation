```mermaid
flowchart LR


tp_winter -->|1| lai_spring
t2m_winter -->|2| lai_spring

tp_winter -->|3| sm_summer
t2m_winter -->|4| sm_summer

tp_winter -->|5| vpd_spring
t2m_winter -->|6| vpd_spring

tp_winter -->|7| vpd_summer
t2m_winter -->|8| vpd_summer

lai_spring -->|9| lai_summer
sm_summer -->|10| lai_summer
vpd_spring --> |11| lai_summer
vpd_summer --> |12| lai_summer

tp_winter -->|13| lai_summer
t2m_winter -->|14| lai_summer

```