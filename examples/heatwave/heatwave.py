import asyncio
import logging

import ray

from agentsociety.configs.agent import AgentClassType
from agentsociety.message import RedisConfig
from agentsociety.metrics import MlflowConfig
from agentsociety.storage import AvroConfig, PostgreSQLConfig

from agentsociety.cityagent import (
    default, SocietyAgent,
)
from agentsociety.configs import (
    AgentsConfig,
    Config,
    EnvConfig,
    ExpConfig,
    LLMConfig,
    MapConfig,
)
from agentsociety.configs.agent import AgentConfig
from agentsociety.configs.exp import WorkflowStepConfig, WorkflowType, MetricExtractorConfig, MetricType
from agentsociety.environment import EnvironmentConfig
from agentsociety.llm import LLMProviderType
from agentsociety.simulation import AgentSociety
from heat_wave_config import Survey1, Survey2, Broadcast1, Broadcast2, normal_run
from heatwave_agent_memory_config import memory_config_societyagent_heatwave

ray.init(logging_level=logging.INFO)

async def need_metric(simulation: AgentSociety):
    # Use function attributes to store counts
    if not hasattr(need_metric, "step_count"):
        setattr(need_metric, "step_count", 0)
    # retrieve infos
    citizen_agents = await simulation.filter(types=(SocietyAgent,))
    hunger_info_gathers = await simulation.gather("hunger_satisfaction", citizen_agents)
    # energy_info_gathers = await simulation.gather("energy_satisfaction", citizen_agents)
    safety_info_gathers = await simulation.gather("safety_satisfaction", citizen_agents)
    social_info_gathers = await simulation.gather("social_satisfaction", citizen_agents)
    # record hunger need of each agent
    for hunger_info_gather in hunger_info_gathers:
        for agent_id, hunger_info in hunger_info_gather.items():
            await simulation.mlflow_client.log_metric(
                key="hunger-satisfaction-" + str(agent_id),
                value=hunger_info,
                step=getattr(need_metric, "step_count"),
            )
    # record energy need of each agent
    # for energy_info_gather in energy_info_gathers:
    #     for agent_id, energy_info in energy_info_gather.items():
    #         await simulation.mlflow_client.log_metric(
    #             key="energy-satisfaction-" + str(agent_id),
    #             value=energy_info,
    #             step=getattr(need_metric, "step_count"),
    #         )
    # record safety need of each agent
    for safety_info_gather in safety_info_gathers:
        for agent_id, safety_info in safety_info_gather.items():
            await simulation.mlflow_client.log_metric(
                key="safety-satisfaction-" + str(agent_id),
                value=safety_info,
                step=getattr(need_metric, "step_count"),
            )
    # record social need of each agent
    for social_info_gather in social_info_gathers:
        for agent_id, social_info in social_info_gather.items():
            await simulation.mlflow_client.log_metric(
                key="social-satisfaction-" + str(agent_id),
                value=social_info,
                step=getattr(need_metric, "step_count"),
            )

    setattr(need_metric, "step_count", getattr(need_metric, "step_count") + 1)

config = Config(
    llm=[
        LLMConfig(
            provider=LLMProviderType.Qwen,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key="TODO",
            model="qwen-plus",
            semaphore=100,
        )
    ],
    env=EnvConfig(
        redis=RedisConfig(
            server="localhost",
            port=6379,
            password="CHANGE_ME",
        ),
        pgsql=PostgreSQLConfig(
            enabled=True,
            dsn="postgresql://postgres:CHANGE_ME@localhost:5432/postgres",
            num_workers="auto",
        ),
        avro=AvroConfig(
            path="avro-output",
            enabled=True,
        ),
        mlflow=MlflowConfig(
            enabled=True,
            mlflow_uri="http://localhost:59000",
            username="admin",
            password="CHANGE_ME",
        ),
    ),
    map=MapConfig(
        file_path="ny_map.pb",
        cache_path="map-cache"
    ),
    agents=AgentsConfig(
        citizens=[
            AgentConfig(
                agent_class=AgentClassType.CITIZEN,
                number=100,
                memory_config_func=memory_config_societyagent_heatwave,
            )
        ],
    ),
    exp=ExpConfig(
        name="heatwave_impact",
        workflow=[
            # ======== base line ========
            normal_run(2),
            Survey2,
            Broadcast1,
            normal_run(1),
            # ======== heat wave begin ========
            WorkflowStepConfig(
                type=WorkflowType.ENVIRONMENT_INTERVENE,
                key="weather",
                value="A severe heatwave has settled over the city, leading to dangerously high temperatures and causing significant difficulties for residents."
            ),
            WorkflowStepConfig(
                type=WorkflowType.ENVIRONMENT_INTERVENE,
                key="temperature",
                value="40 degrees Celsius",
            ),
            normal_run(5),
            Survey2,
            # ======== back to normal ========
            WorkflowStepConfig(
                type=WorkflowType.ENVIRONMENT_INTERVENE,
                key="weather",
                value="The weather is normal and does not affect daily activities"
            ),
            WorkflowStepConfig(
                type=WorkflowType.ENVIRONMENT_INTERVENE,
                key="temperature",
                value="30 degrees Celsius",
            ),
            normal_run(1),
            Survey1,
            Broadcast2,
            normal_run(4),
            Survey2,
        ],
        environment=EnvironmentConfig(
            start_tick=6 * 60 * 60,
        ),
        metric_extractors=[
            MetricExtractorConfig(
                type=MetricType.FUNCTION,
                func=need_metric,
                step_interval=4,
            )
        ],
    ),
)

config = default(config)

async def main():
    agentsociety = AgentSociety(config)
    try:
        await agentsociety.init()
        await agentsociety.run()
    finally:
        await agentsociety.close()
    ray.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
