```mermaid
flowchart LR

tp_winter -->|1| sm_winter
t2m_winter -->|2| sm_winter

sm_winter -->|3| sm_spring

sm_spring -->|4| sm_summer
sm_spring -->|5| lai_spring

lai_spring -->|6| sm_summer
lai_spring -->|7| lai_summer

sm_summer -->|8| lai_summer

tp_winter -->|9| lai_summer
t2m_winter -->|10| lai_summer

tp_winter -->|11| lai_spring
t2m_winter -->|12| lai_spring

```