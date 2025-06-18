import asyncio
import logging

import ray

from agentsociety.cityagent.metrics import mobility_metric

from agentsociety.configs.agent import AgentClassType
from agentsociety.message import RedisConfig
from agentsociety.metrics import MlflowConfig
from agentsociety.storage import AvroConfig, PostgreSQLConfig

from agentsociety.cityagent import (
    default,
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

ray.init(logging_level=logging.INFO)


config = Config(
    llm=[
        LLMConfig(
            provider=LLMProviderType.ZhipuAI,
            base_url="https://open.bigmodel.cn/api/paas/v4/",
            api_key="TODO",
            model="GLM-4-Flash",
            semaphore=200,
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
            path="avro-output.avro",
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
        file_path="beijing_map.pb",
        cache_path="cache"
    ),
    agents=AgentsConfig(
        citizens=[
            AgentConfig(
                agent_class=AgentClassType.CITIZEN,
                number=10,
                memory_from_file="profiles_heatwave-10.json",
            )
        ],
    ),
    exp=ExpConfig(
        name="heatwave_impact",
        workflow=[
            WorkflowStepConfig(
                type=WorkflowType.RUN,
                days=3,
            ),
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
            WorkflowStepConfig(
                type=WorkflowType.RUN,
                days=3,
            ),
            WorkflowStepConfig(
                type=WorkflowType.ENVIRONMENT_INTERVENE,
                key="weather",
                value="The weather is normal and does not affect daily activities"
            ),
            WorkflowStepConfig(
                type=WorkflowType.ENVIRONMENT_INTERVENE,
                key="temperature",
                value="25 degrees Celsius",
            ),
            WorkflowStepConfig(
                type=WorkflowType.RUN,
                days=3,
            ),
        ],
        environment=EnvironmentConfig(
            start_tick=6 * 60 * 60,
        ),
        metric_extractors=[
            MetricExtractorConfig(
                type=MetricType.FUNCTION,
                func=mobility_metric,
                step_interval=10,
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
